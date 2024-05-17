import http.server
import socketserver
import os
import urllib
import cgi
from zipfile import ZipFile
import io
import pandas as pd
from datetime import datetime
import hashlib
import mimetypes
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

try:
    import pwd  # Unix-like systems only
except ImportError:
    import getpass  # Fallback for Windows systems

monitoring_changes = []


def get_file_owner(file_path):
    if os.name == 'posix':
        return pwd.getpwuid(os.stat(file_path).st_uid).pw_name
    else:
        return getpass.getuser()

def get_file_permissions(file_path):
    return oct(os.stat(file_path).st_mode)[-3:]

def get_creation_time(file_path):
    return datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d %H:%M:%S')

def is_file_locked(file_path):
    try:
        with open(file_path, 'a'):
            return False
    except IOError:
        return True

def get_mime_type(file_path):
    type, _ = mimetypes.guess_type(file_path)
    return type or "Unknown"

def get_file_checksum(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def analyze_directory(path):
    file_data = []
    if not os.path.exists(path):
        return file_data
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            size = os.path.getsize(file_path)
            file_data.append({
                'Filename': file,
                'Size (Bytes)': size,
                'Last Modified': datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S'),
                'Created': datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d %H:%M:%S'),
                'Directory': root,
                'Extension': file.split('.')[-1] if '.' in file else "N/A",
                'Owner': get_file_owner(file_path),
                'Permissions': get_file_permissions(file_path),
                'Locked': is_file_locked(file_path),
                'MIME Type': get_mime_type(file_path),
                'Checksum': get_file_checksum(file_path)
            })
    return file_data

def save_to_excel(dataframe, output_path):
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        dataframe.to_excel(writer, index=False, sheet_name='File Details')

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers['content-length'])
        field_data = self.rfile.read(length)
        form = cgi.FieldStorage(
            fp=io.BytesIO(field_data),
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': self.headers['Content-Type']}
        )

        if "delete" in form:
            file_path = form.getvalue("delete")
            try:
                os.remove(file_path)
                monitoring_changes.append(f"Deleted file: {file_path} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                self.send_response(303)
                self.send_header('Location', '/')
                self.end_headers()
            except Exception as e:
                self.send_error(500, f"Failed to delete file: {str(e)}")

        if "rename" in form.keys() and "new_name" in form.keys():
            file_path = form.getvalue("rename")
            new_name = form.getvalue("new_name")
            try:
                new_path = os.path.join(os.path.dirname(file_path), new_name)
                os.rename(file_path, new_path)
                monitoring_changes.append(f"Renamed file: {file_path} to {new_path} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                self.send_response(303)
                self.send_header('Location', '/')
                self.end_headers()
            except Exception as e:
                self.send_error(500, "Failed to rename file: " + str(e))
            return

        if "analyze" in form.keys():
            directory_path = form.getvalue("analyze")
            output_type = form.getvalue("output_type", "web")
            file_data = analyze_directory(directory_path)
            if not file_data:
                self.send_error(404, "Directory not found or no files to analyze.")
                return
            
            if output_type == "excel":
                dataframe = pd.DataFrame(file_data)
                output_path = os.path.join(directory_path, 'analysis_results.xlsx')
                save_to_excel(dataframe, output_path)
                monitoring_changes.append(f"Analyzed directory: {directory_path} and saved results to {output_path} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                self.send_response(303)
                self.send_header('Location', output_path)
                self.end_headers()
            elif output_type == "web":
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(self.render_html(file_data).encode('utf-8'))
                monitoring_changes.append(f"Analyzed directory: {directory_path} and displayed results on web at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            return

        if "download" in form:
            file_path = form.getvalue("download")
            if os.path.isdir(file_path):
                with io.BytesIO() as zip_memory:
                    with ZipFile(zip_memory, 'w') as zip_file:
                        for root, dirs, files in os.walk(file_path):
                            for file in files:
                                file_full_path = os.path.join(root, file)
                                zip_file.write(file_full_path, os.path.relpath(file_full_path, start=os.path.dirname(file_path)))
                    zip_memory.seek(0)
                    self.send_response(200)
                    self.send_header('Content-Disposition', f'attachment; filename="{os.path.basename(file_path)}.zip"')
                    self.send_header('Content-type', 'application/zip')
                    self.end_headers()
                    self.wfile.write(zip_memory.read())
                    monitoring_changes.append(f"Downloaded directory: {file_path} as a ZIP at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                with open(file_path, 'rb') as file:
                    self.send_response(200)
                    self.send_header('Content-Disposition', f'attachment; filename="{os.path.basename(file_path)}"')
                    self.send_header('Content-type', 'application/octet-stream')
                    self.end_headers()
                    self.wfile.write(file.read())
                    monitoring_changes.append(f"Downloaded file: {file_path} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            return

    def render_html(self, file_data):
        html = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>AeroGate Webserver</title>
            <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap" rel="stylesheet">
            <style>
                body { font-family: 'Roboto', sans-serif; padding: 2rem; background: #fff3d0; }
                .container { width: 80%; margin: auto; text-align: center; }
                h1 { color: #333; }
                table { width: 100%; border-collapse: collapse; margin: 20px auto; background-color: #fdfdfd; }
                th, td { padding: 12px; text-align: center; border-bottom: 1px solid #ddd; }
                th { background-color: #A4A5D4; color: white; }
                tr:nth-child(even) { background-color: #f2f2f2; }
                tr:hover { background-color: #dddfe2; }
                .footer { margin-top: 20px; font-size: 12px; text-align: center; color: #888; }
                .monitor-button { margin: 20px 0; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>AeroGate Webserver</h1>
                <h2>File Analysis Results</h2>
                <button class="monitor-button" onclick="location.href='/monitoring'">View Monitoring Changes</button>
                <table>
                    <tr>
                        <th>Filename</th><th>Size (Bytes)</th><th>Last Modified</th><th>Created</th>
                        <th>Directory</th><th>Extension</th><th>Owner</th><th>Permissions</th>
                        <th>Locked</th><th>MIME Type</th><th>Checksum</th>
                    </tr>
        '''
        for file in file_data:
            html += f"<tr><td>{file['Filename']}</td><td>{file['Size (Bytes)']}</td><td>{file['Last Modified']}</td>"
            html += f"<td>{file['Created']}</td><td>{file['Directory']}</td><td>{file['Extension']}</td>"
            html += f"<td>{file['Owner']}</td><td>{file['Permissions']}</td><td>{str(file['Locked'])}</td>"
            html += f"<td>{file['MIME Type']}</td><td>{file['Checksum']}</td></tr>"
        html += '''
                </table>
                <div class="footer">Powered by AeroGate</div>
            </div>
        </body>
        </html>
        '''
        return html

    def render_monitoring_html(self):
        html = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>File Change Monitoring</title>
            <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap" rel="stylesheet">
            <style>
                body { font-family: 'Roboto', sans-serif; padding: 2rem; background: #fff3d0; }
                .container { width: 80%; margin: auto; text-align: center; }
                h1 { color: #333; }
                table { width: 100%; border-collapse: collapse; margin: 20px auto; background-color: #fdfdfd; }
                th, td { padding: 12px; text-align: center; border-bottom: 1px solid #ddd; }
                th { background-color: #A4A5D4; color: white; }
                tr:nth-child(even) { background-color: #f2f2f2; }
                tr:hover { background-color: #dddfe2; }
                .footer { margin-top: 20px; font-size: 12px; text-align: center; color: #888; }
                .home-button { margin: 20px 0; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>File Change Monitoring</h1>
                <h2>Real-time Changes</h2>
                <button class="home-button" onclick="location.href='/'">Go to Home</button>
                <table>
                    <tr><th>Change</th></tr>
        '''
        for change in monitoring_changes:
            html += f"<tr><td>{change}</td></tr>"
        html += '''
                </table>
                <div class="footer">Powered by AeroGate</div>
            </div>
        </body>
        </html>
        '''
        return html

    def do_GET(self):
        if self.path == '/monitoring':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.render_monitoring_html().encode('utf-8'))
        else:
            super().do_GET()

    def list_directory(self, path):
        try:
            list = os.listdir(path)
        except OSError:
            self.send_error(404, "No permission to list directory")
            return None

        list = [item for item in list if item != "http-server.py"]
        list.sort(key=lambda a: a.lower())
        displaypath = urllib.parse.unquote(self.path)
        paths = displaypath.split('/')
        breadcrumb_path = '/'
        breadcrumbs = ['<a href="/">Home</a>']
        for breadcrumb in paths[1:]:
            if breadcrumb:
                breadcrumb_path = os.path.join(breadcrumb_path, breadcrumb)
                breadcrumbs.append(f'&nbsp;&gt;&nbsp;<a href="{breadcrumb_path}">{breadcrumb}</a>')

        r = ['<!DOCTYPE html>', '<html><head>', '<title>AeroGate Webserver</title>',
             '<link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">',
             '<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">',
             '<style>',
             'body { font-family: "Roboto", sans-serif; padding: 0; margin: 0; background: linear-gradient(to right, #fff3d0, #e0ffff); }',
             'h1, h2, h3 { color: #333; }',
             '.navbar { background-color: #A4A5D4; color: white; padding: 10px 20px; }',
             '.navbar a { color: white; text-decoration: none; padding: 0 15px; font-size: 18px; }',
             '.navbar a:hover { text-decoration: underline; }',
             '.content { padding: 20px; }',
             '.welcome { font-size: 24px; margin-top: 20px; color: #204060; }',
             'table { width: 100%; border-collapse: collapse; margin-top: 20px; }',
             'th, td { padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }',
             'a { transition: color 0.3s ease; }',
             'a:hover { color: #ff6347; animation: pulse 1s infinite; }',
             'input[type="submit"], button { transition: background-color 0.3s ease, transform 0.2s ease; }',
             'input[type="submit"]:hover, button:hover { transform: scale(1.05); }',
             'input.delete { background-color: #ff6347; color: white; }',
             'input.delete:hover { background-color: #cc0000; }',
             '</style>',
             '<script>',
             'function searchFiles() {',
             '  var input, filter, table, tr, td, i, txtValue;',
             '  input = document.getElementById("searchInput");',
             '  filter = input.value.toUpperCase();',
             '  table = document.getElementById("filesTable");',
             '  tr = table.getElementsByTagName("tr");',
             '  for (i = 0; i < tr.length; i++) {',
             '    td = tr[i].getElementsByTagName("td")[0];',
             '    if (td) {',
             '      txtValue = td.textContent || td.innerText;',
             '      if (txtValue.toUpperCase().indexOf(filter) > -1) {',
             '        tr[i].style.display = "";',
             '      } else {',
             '        tr[i].style.display = "none";',
             '      }',
             '    }',
             '  }',
             '}',
             '</script>',
             '</head>', '<body>',
             '<div class="navbar">',
             'AeroGate Webserver | ', ' '.join(breadcrumbs),
             '</div>',
             '<div class="content">',
             '<h1>Welcome to AeroGate Web-Server</h1>',
             '<p class="welcome">Manage, Analyze, and Download Your Files Seamlessly!</p>',
             '<form method="post" action="">',
             'Analyze directory: <input type="text" name="analyze" placeholder="Enter directory path" class="form-control">',
             ' Output as: <select name="output_type" class="form-control">',
             '<option value="web">Web Page</option>',
             '<option value="excel">Excel File</option>',
             '</select>',
             '<input type="submit" value="Analyze" class="btn btn-primary mt-2">',
             '</form>',
             '<br/>',
             '<button class="monitor-button" onclick="location.href=\'/monitoring\'">View Monitoring Changes</button>',
             '<br/>',
             '<br/>',
             '<h2>Directory Listing</h2>',
             '<input type="text" id="searchInput" onkeyup="searchFiles()" placeholder="Search for files.." title="Type in a name">',
             '<table id="filesTable">',
             '<tr><th>Name</th><th>Last modified</th><th>Size</th><th>Actions</th></tr>']

        for name in list:
            fullname = os.path.join(path, name)
            displayname = linkname = name
            if os.path.isdir(fullname):
                displayname = name + "/"
                linkname = name + "/"
            r.append('<tr><td><a href="{0}">{1}</a></td>'.format(urllib.parse.quote(linkname), displayname))
            r.append('<td>{0}</td>'.format(self.date_time_string(os.path.getmtime(fullname))))
            size = os.path.getsize(fullname) if not os.path.isdir(fullname) else "-"
            r.append('<td>{0}</td>'.format(size))
            r.append('<td>')
            r.append('<form method="post" action="" style="display: inline;">')
            r.append('<input type="hidden" name="delete" value="{0}">'.format(fullname))
            r.append('<input type="submit" value="Delete" style="background-color: #ff6347; color: white;">')
            r.append('</form> ')
            r.append('<form method="post" action="" style="display: inline;">')
            r.append('<input type="hidden" name="rename" value="{0}">'.format(fullname))
            r.append('<input type="text" name="new_name" placeholder="New name" style="margin-right: 5px;">')
            r.append('<input type="submit" value="Rename" style="background-color: #fdd835; color: black;">')
            r.append('</form> ')
            r.append('<form method="post" action="" style="display: inline;">')
            r.append('<input type="hidden" name="download" value="{0}">'.format(fullname))
            r.append('<input type="submit" value="Download" style="background-color: #4caf50; color: white;">')
            r.append('</form></td></tr>')

        r.append('</table></div></body></html>')

        encoded = ''.join(r).encode('utf-8')
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)
        return None

PORT = 9999

observer = Observer()
observer.start()

with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
    print(f"Serving at port {PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    observer.stop()
observer.join()
