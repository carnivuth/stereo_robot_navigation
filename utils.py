import matplotlib.pyplot as plt

# display image
def imshow(wname,title, img):
    plt.figure(wname); 
    plt.clf()
    plt.imshow(img)
    plt.title(title)
    plt.pause(0.000001)
