#!/usr/bin/env python3


import gi
gi.require_version("Gtk",'3.0')
from gi.repository import Gtk
import os
from rsa import generate_keypair
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
class MainWindow(Gtk.Window):

    epath = Gtk.Entry(**{'placeholder-text':'Plain image path'})
    dpath = Gtk.Entry(**{'placeholder-text':'Encrypted image path'})
    fpath = Gtk.Entry(**{'placeholder-text':'Keys file path'})
    selfemail = Gtk.Entry(**{'placeholder-text': 'Your Email'})
    selfemailpass = Gtk.Entry(**{'placeholder-text': 'Your Email Password'})
    selfemailpass.set_visibility(False)
    servername = Gtk.Entry(**{'placeholder-text': 'Server name'})
    serverport = Gtk.Entry(**{'placeholder-text': 'Port'})

    imagepath = Gtk.Entry(**{'placeholder-text': 'Image File Name'})
    keyfilepath = Gtk.Entry(**{'placeholder-text': 'Key File Name'})
    to = Gtk.Entry(**{'placeholder-text': 'To'})
    itercount = Gtk.Entry(**{'placeholder-text': 'Itercount'})
    pkeys = Gtk.Entry(**{'placeholder-text': 'Public Keys'})


    p = Gtk.Entry()
    q = Gtk.Entry()
    e = Gtk.Entry(**{'placeholder-text':'e'})
    en_n = Gtk.Entry(**{'placeholder-text':'n'})
    d = Gtk.Entry(**{'placeholder-text':'d'})
    de_n = Gtk.Entry(**{'placeholder-text':'n'})
    en_rsa = Gtk.CheckButton()
    de_rsa = Gtk.CheckButton()
    ifield = Gtk.Entry(text = '1', xalign = 1)

    def SendMail(Self,Widget):
        try:
            ImgFileName = Self.imagepath
            Keypath = Self.keyfilepath
            itercount = Self.itercount
            From = Self.selfemail
            To = Self.to
            Key = Self.pkeys
            Server = Self.servername
            Port = Self.serverport
            UserPassword = Self.selfemailpass


            with open(ImgFileName.get_text(), 'rb') as f:
                img_data = f.read()

            msg = MIMEMultipart()
            msg['Subject'] = itercount.get_text()
            msg['From'] = From.get_text()
            msg['To'] = To.get_text()


            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload(open(Keypath.get_text(), 'rb').read())
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(Keypath.get_text()))



            text = MIMEText(
                "Public Key Code > d: " + Key.get_text().split(",")[0] + " , n: " + Key.get_text().split(",")[1])
            msg.attach(text)
            image = MIMEImage(img_data, name=os.path.basename(ImgFileName.get_text()))
            msg.attach(image)
            msg.attach(attachment)
            s = smtplib.SMTP(Server.get_text(), Port.get_text())
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(From.get_text(), UserPassword.get_text())
            s.sendmail(From.get_text(), To.get_text(), msg.as_string())
            s.quit()
            dialog = Gtk.MessageDialog(Self, 0, Gtk.MessageType.INFO,
                                       Gtk.ButtonsType.OK, "Success")
            dialog.format_secondary_text("Sended Message")
            dialog.run()
            dialog.destroy()
        except Exception as e:
            dialog = Gtk.MessageDialog(Self, 0, Gtk.MessageType.INFO,
                                       Gtk.ButtonsType.OK, "Error")
            dialog.format_secondary_text("Error Sended Message")
            dialog.run()
            dialog.destroy()



    def __init__(self):
        Gtk.Window.__init__(self, title = "Image Encryption/Decryption using Rubik's Cube")
        self.set_default_size(600, 300)
        mainBox = Gtk.Box(orientation= Gtk.Orientation.VERTICAL, spacing = 10)
        self.add(mainBox)
        self.servername.set_text("smtp.gmail.com")
        self.serverport.set_text("587")
        mainArea = Gtk.Stack()
        mainArea.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        mainArea.set_transition_duration(200)

        firstBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        mainArea.add_titled(firstBox, "encryption", "Encryption")

        hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        label = Gtk.Label("Input image path")
        button = Gtk.Button()
        image = Gtk.Image.new_from_icon_name("folder", Gtk.IconSize.MENU)
        button.add(image)
        button.connect("clicked", self.on_open_encrypt)
        hbox.pack_start(label, False, True, 10)
        hbox.pack_end(self.epath, False, True, 10)
        hbox.pack_end(button, False, True, 0)
        firstBox.pack_start(hbox, False, True, 10)

        hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        label = Gtk.Label("Max Iterations")
        hbox.pack_start(label, False, True, 10)
        hbox.pack_end(self.ifield, False, True, 10)
        firstBox.pack_start(hbox, False, True, 0)

        hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        label = Gtk.Label("Encrypt Keys using RSA")
        hbox.pack_start(self.en_rsa, False, True, 2)
        hbox.pack_start(label, False, True, 0)
        hbox.pack_end(self.en_n, False, True, 10)
        hbox.pack_end(self.e, False, True, 10)
        firstBox.pack_start(hbox, False, True, 0)

        buttonBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        button = Gtk.Button.new_with_label('Encrypt')
        button.connect("clicked", self.on_encrypt)
        buttonBox.set_center_widget(button)
        firstBox.pack_end(buttonBox, False, True, 0)

    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


        secondBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10)
        mainArea.add_titled(secondBox, "decryption", "Decryption")

        hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        label = Gtk.Label("Input image path")
        button = Gtk.Button()
        image = Gtk.Image.new_from_icon_name("folder", Gtk.IconSize.MENU)
        button.add(image)
        button.connect("clicked", self.on_open_decrypt)
        hbox.pack_start(label, False, True, 10)
        hbox.pack_end(self.dpath, False, True, 10)
        hbox.pack_end(button, False, True, 0)
        secondBox.pack_start(hbox, False, True, 10)

        hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        label = Gtk.Label("Keys/MAX_ITER file path")
        button = Gtk.Button()
        image = Gtk.Image.new_from_icon_name("folder", Gtk.IconSize.MENU)
        button.add(image)
        button.connect("clicked", self.on_open_file)
        hbox.pack_start(label, False, True, 10)
        hbox.pack_end(self.fpath, False, True, 10)
        hbox.pack_end(button, False, True, 0)
        secondBox.pack_start(hbox, False, True, 0)

        hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        label = Gtk.Label("Decrypt Keys")
        hbox.pack_start(self.de_rsa, False, True, 2)
        hbox.pack_start(label, False, True, 0)
        hbox.pack_end(self.de_n, False, True, 10)
        hbox.pack_end(self.d, False, True, 10)
        secondBox.pack_start(hbox, False, True, 0)

        buttonBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        button = Gtk.Button.new_with_label('Decrypt')
        button.connect("clicked", self.on_decrypt)
        buttonBox.set_center_widget(button)
        secondBox.pack_end(buttonBox, False, True, 10)


#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

        thirdBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10)
        mainArea.add_titled(thirdBox, "generate", "Key Generation")

        hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        label = Gtk.Label("Prime number 1")
        hbox.pack_start(label, False, True, 10)
        hbox.pack_end(self.p, False, True, 10)
        thirdBox.pack_start(hbox, False, True, 0)

        hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        label = Gtk.Label("Prime number 2")
        hbox.pack_start(label, False, True, 10)
        hbox.pack_end(self.q, False, True, 10)
        thirdBox.pack_start(hbox, False, True, 0)

        buttonBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        button = Gtk.Button.new_with_label('Generate')
        button.connect("clicked", self.on_generate)
        buttonBox.set_center_widget(button)
        thirdBox.pack_end(buttonBox, False, True, 10)

  # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


        fourthbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        mainArea.add_titled(fourthbox, "send", "Send Email")
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        label = Gtk.Label("Email Settings")
        hbox.pack_start(label, False, True, 10)
        fourthbox.pack_start(hbox, False, True, 0)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        label = Gtk.Label("Your Email")
        hbox.pack_start(label, False, True, 10)
        hbox.pack_end(self.selfemail, False, True, 10)
        fourthbox.pack_start(hbox, False, True, 0)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        label = Gtk.Label("Your Email Password")
        hbox.pack_start(label, False, True, 10)
        hbox.pack_end(self.selfemailpass, False, True, 10)
        fourthbox.pack_start(hbox, False, True, 0)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        label = Gtk.Label("Server Name")
        hbox.pack_start(label, False, True, 10)
        hbox.pack_end(self.servername, False, True, 10)
        fourthbox.pack_start(hbox, False, True, 0)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        label = Gtk.Label("Port")
        hbox.pack_start(label, False, True, 10)
        hbox.pack_end(self.serverport, False, True, 10)
        fourthbox.pack_start(hbox, False, True, 0)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        label = Gtk.Label("Image Name")
        button = Gtk.Button()
        image = Gtk.Image.new_from_icon_name("folder", Gtk.IconSize.MENU)
        button.add(image)
        button.connect("clicked", self.on_open_image)
        hbox.pack_start(label, False, True, 10)
        hbox.pack_end(self.imagepath, False, True, 10)
        hbox.pack_end(button, False, True, 0)
        fourthbox.pack_start(hbox, False, True, 0)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        label = Gtk.Label("Key File")
        button = Gtk.Button()
        keyfiles = Gtk.Image.new_from_icon_name("folder", Gtk.IconSize.MENU)
        button.add(keyfiles)
        button.connect("clicked", self.on_open_key)
        hbox.pack_start(label, False, True, 10)
        hbox.pack_end(self.keyfilepath, False, True, 10)
        hbox.pack_end(button, False, True, 0)
        fourthbox.pack_start(hbox, False, True, 0)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        label = Gtk.Label("Itercount")
        hbox.pack_start(label, False, True, 10)
        hbox.pack_end(self.itercount, False, True, 10)
        fourthbox.pack_start(hbox, False, True, 0)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        label = Gtk.Label("Public Keys")
        hbox.pack_start(label, False, True, 10)
        hbox.pack_end(self.pkeys, False, True, 10)
        fourthbox.pack_start(hbox, False, True, 0)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        label = Gtk.Label("To")
        hbox.pack_start(label, False, True, 10)
        hbox.pack_end(self.to, False, True, 10)
        fourthbox.pack_start(hbox, False, True, 0)

        buttonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        button = Gtk.Button.new_with_label('Send Email') # Save yapican daha
        button.connect("clicked", self.SendMail)
        buttonBox.set_center_widget(button)
        fourthbox.pack_end(buttonBox, False, True, 10)


        stackSwitcher = Gtk.StackSwitcher()
        stackSwitcher.set_stack(mainArea)
        switcherBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        switcherBox.set_center_widget(stackSwitcher)
        mainBox.pack_start(switcherBox, False, True, 0)
        mainBox.pack_start(mainArea, False, True, 0)

    def on_open_image(self, widget):
        dialog = Gtk.FileChooserDialog("Select input image", self, Gtk.FileChooserAction.OPEN,
        ("Cancel", Gtk.ResponseType.CANCEL, "Open", Gtk.ResponseType.OK))
        response = dialog.run()
        if(response ==  Gtk.ResponseType.OK):
            self.imagepath.set_text(dialog.get_filename())
        dialog.destroy()

    def on_open_key(self, widget):
        dialog = Gtk.FileChooserDialog("Select input image", self, Gtk.FileChooserAction.OPEN,
        ("Cancel", Gtk.ResponseType.CANCEL, "Open", Gtk.ResponseType.OK))
        response = dialog.run()
        if(response ==  Gtk.ResponseType.OK):
            self.keyfilepath.set_text(dialog.get_filename())
        dialog.destroy()

    def on_open_encrypt(self, widget):
        dialog = Gtk.FileChooserDialog("Select input image", self, Gtk.FileChooserAction.OPEN,
        ("Cancel", Gtk.ResponseType.CANCEL, "Open", Gtk.ResponseType.OK))
        response = dialog.run()
        if(response ==  Gtk.ResponseType.OK):
            self.epath.set_text(dialog.get_filename())
        dialog.destroy()

    def on_open_decrypt(self, widget):
        dialog = Gtk.FileChooserDialog("Select input image", self, Gtk.FileChooserAction.OPEN,
        ("Cancel", Gtk.ResponseType.CANCEL, "Open", Gtk.ResponseType.OK))
        response = dialog.run()
        if(response ==  Gtk.ResponseType.OK):
            self.dpath.set_text(dialog.get_filename())
        dialog.destroy()

    def on_open_file(self, widget):
        dialog = Gtk.FileChooserDialog("Select input image", self, Gtk.FileChooserAction.OPEN,
        ("Cancel", Gtk.ResponseType.CANCEL, "Open", Gtk.ResponseType.OK))
        response = dialog.run()
        if(response ==  Gtk.ResponseType.OK):
            self.fpath.set_text(dialog.get_filename())
        dialog.destroy()

    def on_error(self, message=''):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
            Gtk.ButtonsType.CANCEL, "Error")
        if(message!=''):
            dialog.format_secondary_text(message)     
        else:
            dialog.format_secondary_text("An error occured while processing. Please check the inputs")
        dialog.run()
        dialog.destroy()
    
    def on_success(self):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
            Gtk.ButtonsType.OK, "Success")
        dialog.format_secondary_text(
            "Process run successfully")
        dialog.run()
        dialog.destroy()

    def on_encrypt(self, widget):
        if(not self.ifield.get_text().isdigit()):
            self.on_error("Max iterations must be a number")
            return
        if(self.epath.get_text() == ''):
            self.on_error("Enter path and try again")
            return
        command = 'python3 encrypt.py ' + self.epath.get_text()+ ' ' + self.ifield.get_text()
        if(self.en_rsa.get_active()):
            command = command + ' ' + self.e.get_text() + ' ' + self.en_n.get_text()
        if(os.system(command) != 0):
            self.on_error()
        else:
            self.on_success()

    def on_decrypt(self, widget):
        if(self.dpath.get_text() == '' or self.fpath.get_text() == ''):
            self.on_error("Enter path and try again")
            return
        command = 'python3 decrypt.py ' + self.dpath.get_text()
        if(self.de_rsa.get_active()):
            command = command + ' ' + self.d.get_text() + ' ' + self.de_n.get_text()
        command = command + ' < ' + self.fpath.get_text()
        if(os.system(command) != 0):
            self.on_error()
        else:
            self.on_success()
    
    def on_generate(self, widget):
        p = self.p
        q = self.q
        if(p.get_text() == '' or q.get_text() == '' or 
            not p.get_text().isdigit() or not q.get_text().isdigit()):
            self.on_error("Check inputs again")
            return
        try:
            pu, pr = generate_keypair(int(p.get_text()), int(q.get_text()))
        except:
            self.on_error("Check inputs again")
            return
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
            Gtk.ButtonsType.OK, "Success")
        dialog.format_secondary_text(
            "Public Key: " + str(pu[0]) + ', ' + str(pu[1]) +
            "\nPrivate Key: " + str(pr[0]) + ', ' + str(pr[1]))
        dialog.run()
        dialog.destroy()

win = MainWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
