# import base64
# imgstring = '''data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/'''
# I7vqQpRnDKpjUYG0MUCcdWS3xgI6qYG2
# 2021-04-06 09:00:00

# imgtype = imgstring.split(",")[0].split("/")[1].split(";")[0]
# if(imgtype in ['jpeg','jpg','png']):
#   imgdata = base64.b64decode(imgstring.split(",")[1])
#   filename = 'some_image.jpg'  # I assume you have a way of picking unique filenames
#   with open(filename, 'wb') as f:
#       f.write(imgdata)


'''
<!DOCTYPE html>
<html>
<body>

<script>
/******************for base 64 *****************************/
function uploadFile(inputElement) {
  var file = inputElement.files[0];
  var reader = new FileReader();
  reader.onloadend = function() {
    console.log('Encoded Base 64 File String:', reader.result);
    
    /******************* for Binary ***********************/
    var data=(reader.result).split(',')[1];
     var binaryBlob = atob(data);
     //console.log('Encoded Binary File String:', binaryBlob);
  }
  reader.readAsDataURL(file);
}
</script>

<h1>Show File-select Fields</h1>

<h3>Show a file-select field which allows only one file to be chosen:</h3>
<form action="/action_page.php">
  <label for="myfile">Select a file:</label>
  <input type="file" id="myfile" name="myfile" onChange="uploadFile(this)"><br><br>
  <input type="submit">
</form>

<h3>Show a file-select field which allows multiple files:</h3>
<form action="/action_page.php">
  <label for="myfile">Select files:</label>
  <input type="file" id="myfile" name="myfile" onChange="uploadFile(this)" multiple><br><br>
  <input type="submit">
</form>

</body>
</html>

'''

# Send email
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import smtplib
import ssl


def home(subj="Recover password", mess="messaggio"):
    print('ciao')
    try:
        port = 465  # For SSL
        # Create a secure SSL context
        context = ssl.create_default_context()
        mail_server = 'smtp.gmail.com'
        mail_username = '***************'
        mail_password = '***************'

        with smtplib.SMTP_SSL(mail_server, port, context=context) as server:
            server.login(mail_username, mail_password)
            # TODO: Send email here
            sender_email = '***************'
            receiver_email = '***************'
            message = """\
Subject: {}

{}""".format(subj, mess)
            server.sendmail(sender_email, receiver_email, message)
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    return "Email Sent"


def send_email(obj, msg, receiver):
    message = Mail(
        from_email='***************',
        to_emails=receiver,
        subject=obj,
        html_content='<div>{}<a href="{}">Reset Password</a></div>'.format("Clicca questo link per resettare la tua password: ", "http://localhost:5000/api/user/resetPassword?language=it&id=1&tokenPass=0CrIk30JrX8ABqskqS8m8EMyI2DQnmww"))
    try:
        sg = SendGridAPIClient(
            '*************************************')
        response = sg.send(message)
        print(response.status_code, flush=True)
        print(response.body, flush=True)
        print(response.headers, flush=True)
    except Exception as e:
        print(e.message, flush=True)


if __name__ == "__main__":
    send_email("Oggetto", "", "***************")
