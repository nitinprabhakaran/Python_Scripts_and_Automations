import qrcode
import image

qr = qrcode.QRCode(
    version = 15,   # Here 15 means the version of QR Code, higher the number, more complex is the QR
    box_size = 10,
    border = 5
)

data = input("Enter the URL for which the QR is to be generated : ")
qr.add_data(data)
qr.make(fit=True)
img = qr.make_image(fill='black',back_color='white')
img.save("QRCode.jpg")