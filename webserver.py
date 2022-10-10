from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import smtplib

class RequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        json_body = json.loads(post_body)
        
        response = self.sendEmail(json_body['sender'], json_body['receiver'], json_body['body'])
        
        self.send_response(200)
        self.send_header('content-type', 'test/html')
        self.end_headers()
        self.wfile.write(bytes(json.dumps(response), "utf-8"))

    def sendEmail(self, sender, receiver, body):
        try:
            smtpObj = smtplib.SMTP('smtp.gmail.com')
            response = smtpObj.sendmail(sender, [receiver], body)         
            print("Successfully sent email")
            return response
        except Exception as e:
            print(f"Error: unable to send email {e}")
            return str(e)



def main():
    PORT = 8000
    server = HTTPServer(('', PORT), RequestHandler)
    print('Server is running on port %s', PORT)
    server.serve_forever()


if __name__ == '__main__':
    main()