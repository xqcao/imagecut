from flask import Flask,request,render_template,send_file
import os
from io import BytesIO
from PIL import Image, ImageDraw

app = Flask('__name__')

@app.route('/',methods=['GET','POST'])
def brforeUpload():
    print('page load ...')
    message='please upload your image'
    return render_template('imgUploadMemory.html',msg=message)

@app.route('/memoryimg',methods=['POST','GET'])
def DomemoryProcess():
    if request.method == 'POST' and 'photo' in request.files:
        oneimage = request.files['photo']
        # in_memory_io = BytesIO()
        # ff.save(in_memory_io)
        imageData =Image.open(oneimage)
        
        
        draw = ImageDraw.Draw(imageData)
        byte_io = BytesIO()
        imageData.save(byte_io, 'PNG')
        byte_io.seek(0)
    return send_file(byte_io, mimetype='image/png')

@app.route('/passportimg',methods=['POST','GET'])
def DoPassportMemory():
    # SQUARE_FIT_SIZE=300
    sq=600
    bgbase = Image.new('RGB',(sq*3,sq*2),'white')
    if request.method == 'POST' and 'photo' in request.files:
        oneimage = request.files['photo']
        imageData =Image.open(oneimage)
        iw,ih = imageData.size
        if iw>ih:
            cp_img_h = int((sq/iw)*ih)
            cp_img_w = sq
        else:
            cp_img_w = int((sq/ih)*iw)
            cp_img_h = sq
        im = imageData.resize((cp_img_w,cp_img_h))
        print('im size',im.size)
        bgbase.paste(im,(0,0))
        bgbase.paste(im,(cp_img_w,0))
        bgbase.paste(im,((cp_img_w*2),0))
        bgbase.paste(im,(0,cp_img_h))
        bgbase.paste(im,(cp_img_w,cp_img_h))
        bgbase.paste(im,((cp_img_w*2),cp_img_h))
        
        draw = ImageDraw.Draw(bgbase)
        byte_io = BytesIO()
        bgbase.save(byte_io, 'PNG')
        byte_io.seek(0)
    return send_file(byte_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)