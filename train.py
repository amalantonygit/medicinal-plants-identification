import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from matplotlib import pyplot
from keras.applications.vgg16 import VGG16
from keras.models import Model
from keras.layers import Dense
from keras.layers import Flatten
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.utils.vis_utils import plot_model

# define vgg16 model from Keras
def define_model():
    # load model
    model = VGG16(include_top=False, input_shape=(224, 224, 3))
    # mark loaded layers as not trainable
    for layer in model.layers:
        layer.trainable = False
    # add new classifier layers
    flat1 = Flatten()(model.layers[-1].output)
    class1 = Dense(128, activation='relu', kernel_initializer='he_uniform')(flat1)
    output = Dense(10, activation='softmax')(class1)
    # define new model
    model = Model(inputs=model.inputs, outputs=output)
    # compile model
    opt=Adam(0.001)
    model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
    return model
 
# plot diagnostic learning curves
def summarize_diagnostics(history):
    # plot loss
    pyplot.subplot(211)
    pyplot.title('Cross Entropy Loss')
    pyplot.plot(history.history['loss'], color='blue', label='train')
    pyplot.plot(history.history['val_loss'], color='orange', label='test')
    # plot accuracy
    pyplot.subplot(212)
    pyplot.title('Classification Accuracy')
    pyplot.plot(history.history['accuracy'], color='blue', label='train')
    pyplot.plot(history.history['val_accuracy'], color='orange', label='test')
    # save plot to file
    pyplot.savefig('plots/loss_accuracy_plot.png')
    pyplot.close()
 
# run the test harness for evaluating a model
def run_test_harness():
    # define model
    model = define_model()
    # create data generator
    #set validation split as 20%
    train_datagen = ImageDataGenerator(rescale=1.0/255.0,
    rotation_range=20,
    zoom_range=0.15,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.15,
    horizontal_flip=True,
    fill_mode="nearest",
    validation_split=0.20)
    #specify imagenet mean values for centering
    train_datagen.mean = [123.68, 116.779, 103.939]
    train_generator = train_datagen.flow_from_directory('dataset',
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    subset='training') # set as training data
    validation_generator = train_datagen.flow_from_directory(
    'dataset',
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    subset='validation',seed=101)#set as validation data
    model.summary()
    plot_model(model, to_file='plots/layers_plot.png')
    checkpoint = ModelCheckpoint("models/vgg16{val_accuracy:.2f}.h5", monitor='val_accuracy', verbose=1, save_best_only=True, save_weights_only=False, mode='auto', period=1)
    early = EarlyStopping(monitor='val_accuracy', min_delta=0, patience=40, verbose=1, mode='auto')
    # fit model
    history = model.fit_generator(train_generator, steps_per_epoch=len(train_generator),
        validation_data=validation_generator, validation_steps=len(validation_generator), epochs=100, verbose=1,callbacks=[early,checkpoint])
    # learning curves
    summarize_diagnostics(history)
    print("Training completed.")
# entry point, run the test harness
run_test_harness()