from keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models, callbacks, optimizers

base_dir = r'RPS_dataset'
image_size = (200, 300)


# enables stopping training when a desired accuracy is reached to prevent over-fitting
class accuracy_cutoff(callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        if logs.get('accuracy') >= 0.98:
            print('\nTraining stopped after accuracy reached = %2.2f%%' % (logs['accuracy'] * 100))
            self.model.stop_training = True


# helps generate data by transforming existing images (rescale shift rotation etc) and determines how much will be set aside for validation
generated_data = ImageDataGenerator(rescale=1. / 255, rotation_range=20, vertical_flip=True, horizontal_flip=True,
                                    shear_range=0.2, fill_mode='wrap', validation_split=0.2)
train_data = generated_data.flow_from_directory(base_dir, target_size=image_size, class_mode='categorical',
                                                subset='training', shuffle=True)
val_data = generated_data.flow_from_directory(base_dir, target_size=image_size, class_mode='categorical',
                                              subset='validation', shuffle=True)

model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(200, 300, 3)),
    layers.MaxPooling2D(2, 2),
    layers.Dropout(0.2),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D(2, 2),
    layers.Dropout(0.2),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D(2, 2),
    layers.Dropout(0.2),
    layers.Conv2D(256, (3, 3), activation='relu'),
    layers.MaxPooling2D(2, 2),
    layers.Dropout(0.2),
    layers.Conv2D(512, (3, 3), activation='relu'),
    layers.MaxPooling2D(2, 2),
    layers.Dropout(0.2),
    layers.Conv2D(756, (3, 3), activation='relu'),
    layers.MaxPooling2D(2, 2),
    layers.Dropout(0.2),
    layers.Flatten(),
    layers.Dense(1024, activation='relu'),
    layers.Dense(3, activation='softmax')
])

model.compile(
    loss='categorical_crossentropy',
    optimizer=optimizers.Adam(),
    metrics=['accuracy']
)

fitted_model = model.fit(

    train_data,
    validation_data=val_data,
    steps_per_epoch=40,
    epochs=50,
    batch_size=64,
    callbacks=[accuracy_cutoff()]  # enable this for accuracy cutoff
)

model.save('model_saved.h5')
