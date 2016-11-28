import os
from flask import Flask,request,render_template,send_file
from io import BytesIO
from PIL import Image, ImageDraw

app = Flask('__name__')

@app.route('/',methods=['GET','POST'])
def brforeUpload():
    print('page load ...')
    message='please upload your image'
    return render_template('imgUploadMemory.html',msg=message)
    
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
            ex_p_x = int((iw-ih)/2)
            im0 = imageData.crop((ex_p_x,0,(ih+ex_p_x),ih))
        else:
            ex_p_y = int((ih-iw)/2)
            im0 = imageData.crop((0,ex_p_y,iw,(iw+ex_p_y)))
        im = im0.resize((600,600))
        bgbase.paste(im,(0,0))
        bgbase.paste(im,(600,0))
        bgbase.paste(im,((600*2),0))
        bgbase.paste(im,(0,600))
        bgbase.paste(im,(600,600))
        bgbase.paste(im,((600*2),600))
        
        draw = ImageDraw.Draw(bgbase)
        byte_io = BytesIO()
        bgbase.save(byte_io, 'PNG')
        byte_io.seek(0)
    return send_file(byte_io, mimetype='image/png')

if __name__ == '__main__':
    port=int(os.environ.get('PORT',5000))
    app.run(host='0.0.0.0',port=port)