import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

# create data generator
#set validation split as 20%
image_datagen = ImageDataGenerator(rescale=1.0/255.0,
    validation_split=0.20)
train_generator = image_datagen.flow_from_directory('dataset',
target_size=(224, 224),
batch_size=32,
class_mode='categorical',
subset='training')# set as training data
validation_generator = image_datagen.flow_from_directory(
'dataset',
target_size=(224, 224),
batch_size=32,
class_mode='categorical',
subset='validation',seed=101,shuffle=False)#set as validation data

#load saved model
saved_model = load_model("models/cnn0.83.h5")

# predict probabilities for test set
pred_probs = saved_model.predict(validation_generator, verbose=0)
# predict classes for test set
pred_classes =pred_probs.argmax(1)
actual_classes = validation_generator.classes
accuracy = accuracy_score(actual_classes, pred_classes)
print('Accuracy: %.2f' % accuracy)
# precision: tp / (tp + fp)
precision = precision_score(actual_classes, pred_classes,average='weighted')
print('Precision: %.2f' % precision)
# recall: tp / (tp + fn)
recall = recall_score(actual_classes, pred_classes,average='weighted')
print('Recall: %.2f' % recall)
# f1: 2 tp / (2 tp + fp + fn)
f1 = f1_score(actual_classes, pred_classes,average='weighted')
print('F1 score: %.2f' % f1)
#plot the confusion matrix and write it to a file
matrix = confusion_matrix(actual_classes, pred_classes)
df_cm = pd.DataFrame(matrix, range(10), range(10))
sn.set(font_scale=1.4) # for label size
## font size and colour map for the plot
cm_plot=sn.heatmap(df_cm, annot=True, annot_kws={"size": 16},cmap="BuPu") 
cm_plot.set_yticklabels(cm_plot.get_yticklabels(), rotation=90)
cm_plot.set_xticklabels(cm_plot.get_xticklabels(), rotation=0)
plt.show()
print(classification_report(actual_classes,pred_classes))
