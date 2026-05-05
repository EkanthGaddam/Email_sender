
from flask import Flask,render_template,redirect,request,flash,url_for,session,jsonify
from email.mime.text import MIMEText
import smtplib
import pandas as pd
import sys,pathlib
import os


ASSETS_DIR = os.path.dirname(os.path.abspath(__file__))

parent_dir = pathlib.Path(__file__).parent
sys.path.append(str(parent_dir))
APITimeout = 60
app = Flask(__name__,static_folder="static")
@app.route('/')
def index():
    return render_template("index.html")


@app.route("/upload_excel", methods=["POST"])
def upload_excel():
    # 'file' must match the name attribute in your HTML input
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    
    if file and file.filename.endswith((".xlsx", ".xls")):
        try:
            # Load the Excel data
            df = pd.read_excel(file)
            template_file=request.files['template_file']
            template_content = template_file.read().decode("utf-8")
            if template_content=='':
                flash("Choose template")
                return render_template("index.html")
            # Extract email list (assuming column header is 'Email')
            # 1. Convert Serial Number to string
            df['Serial Number'] = df['slno'].astype(str)

            # 2. Fill empty email cells with an empty string
            df['Email'] = df['Email'].fillna('')

            # 3. NOW extract the list (everything is now a string)
            emails = df['Email'].tolist()

            emailList=emails
           # 1. Define your variables (Replace with your actual values)
            FromEmailAddress = "gaddamyekanth3170@gmail.com"
            PasswordEmail = "wgbcaflcqsnrecgp"  # Use a Google App Password
            ToEmailAddress = emailList
            # ToEmailAddress="ekanthgaddam25@gmail.com"
            SubjectEmail = "test"

            # 2. Setup the connection (Note the comma after the host)
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
                smtp_server.login(FromEmailAddress, PasswordEmail)

                # 3. Load your template file
                html_content = template_content
                # 4. Use the template directly as the body
                msg = MIMEText(html_content, "html")
                msg['Subject'] = SubjectEmail
                msg['From'] = FromEmailAddress
                
                # Split the string into a list for the 'to' field
                # toEmailList = ToEmailAddress.split(";")
                msg['To'] = ", ".join(ToEmailAddress)

                # 5. Send the email
                smtp_server.sendmail(FromEmailAddress, ToEmailAddress, msg.as_string())
        except (smtplib.SMTPConnectError, OSError):
            # Triggered if there is no internet or server is unreachable
            flash("Failed to connect. Please check your internet connection.", "error")
            return render_template("index.html")
        except KeyError:
            # Catch the specific error when 'Email' is missing
            flash("Error: The uploaded sheet is missing the required Email Field")
            return render_template("index.html")
        except Exception as e:
            ''
    
            
    else:
        flash("Please select the excel sheet.")
        return render_template("index.html")
    return render_template("index.html")
        


    


if __name__ == '__main__':
    app.secret_key="MCI9876543210"
    app.run(host="192.168.29.24",port=5000,debug=True) 