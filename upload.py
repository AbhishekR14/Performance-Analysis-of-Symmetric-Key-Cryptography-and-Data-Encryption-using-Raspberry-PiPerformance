from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

import yagmail



def Upload_file(key, emailv,filename):
    
    
    
    gauth = GoogleAuth()
    
    gauth.LoadCredentialsFile("mycreds.txt")
    
    if gauth.credentials is None:
    
        gauth.GetFlow()
        gauth.flow.params.update({'access_type': 'offline'})
        gauth.flow.params.update({'approval_prompt': 'force'})
    
        gauth.LocalWebserverAuth()
    
    elif gauth.access_token_expired:
    
    
        gauth.Refresh()
    else:
    
        gauth.Authorize()
    
    gauth.SaveCredentialsFile("mycreds.txt")  
    
    drive = GoogleDrive(gauth)
    

    enc_filelist = os.listdir("encrypted_files")
    
    for upload_file in enc_filelist:
        
        if(filename in upload_file):
            gfile = drive.CreateFile({'title': upload_file})
            gfile.SetContentFile(os.path.join('encrypted_files',upload_file))
            gfile.Upload()
            file_details = 'The file name is : '+ upload_file+'\n' +'The key is : '+key+ '\nThe File Id is: '+gfile['id']
            #print(file_details)
        
            server = yagmail.SMTP(user = "capstoneproject0621@gmail.com",  password = "presentation0621")
        
            server.send(to=emailv,subject= "Encrypted file details",contents=file_details,)
        else:
            continue
#Upload_file("sidsunil7@gmail.com")
