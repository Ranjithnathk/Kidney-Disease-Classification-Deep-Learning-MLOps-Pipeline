import os
import urllib.request as request
from zipfile import ZipFile
import tensorflow as tf
from pathlib import Path
from KidneyDiseaseClassifier.entity.config_entity import PrepareBaseModelConfig


class PrepareBaseModel:
    def __init__(self, config: PrepareBaseModelConfig):
        self.config = config

    
    def get_base_model(self):
        self.model = tf.keras.applications.InceptionV3(
            input_shape=self.config.params_image_size,
            weights="imagenet",
            include_top=self.config.params_include_top
        )

        self.save_model(path=self.config.base_model_path, model=self.model)

    

    @staticmethod
    def _prepare_full_model(model, classes, freeze_all, freeze_till, learning_rate, input_shape):
    # Freeze base model layers
        model.trainable = True
        for layer in model.layers:
            layer.trainable = False
        for layer in model.layers[-100:]: 
            layer.trainable = True

        inputs = tf.keras.Input(shape=input_shape)
        x = model(inputs, training=False)
        x = tf.keras.layers.GlobalAveragePooling2D()(x)
        x = tf.keras.layers.Dense(512, activation='relu')(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.Dropout(0.5)(x)
        x = tf.keras.layers.Dense(256, activation='relu')(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.Dropout(0.5)(x)
        x = tf.keras.layers.Dense(128, activation='relu')(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.Dropout(0.5)(x)
        outputs = tf.keras.layers.Dense(units=classes, activation='softmax')(x)

        full_model = tf.keras.models.Model(inputs=inputs, outputs=outputs)

        full_model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
            loss=tf.keras.losses.CategoricalCrossentropy(),
            metrics=["accuracy"]
        )

        return full_model
    
    
    def update_base_model(self):
        self.full_model = self._prepare_full_model(
            model=self.model,
            classes=self.config.params_classes,
            freeze_all=False,
            freeze_till=None,
            learning_rate=self.config.params_learning_rate,
            input_shape=self.config.params_image_size
        )

        self.save_model(path=self.config.updated_base_model_path, model=self.full_model)

    
        
    @staticmethod
    def save_model(path: Path, model: tf.keras.Model):
        path = str(path)
        if not path.endswith(".keras"):
            path += ".keras"
        model.save(path, include_optimizer=False) # Save full model
        print(f"Model saved to {path}")



