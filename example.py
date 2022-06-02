import tensorflow as tf
mnist = tf.keras.datasets.mnist

def get_model_a():
    return tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(10, activation='softmax')
    ])


def get_model_b():
    return tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(128, activation='relu'),
    #tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(10, activation='softmax')
    ])


def evaluate(model, seed=0):
    tf.random.set_seed(seed)
    (x_train, y_train),(x_test, y_test) = mnist.load_data()
    x_train, x_test = x_train / 255.0, x_test / 255.0

    model.compile(optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])

    model.fit(x_train, y_train, epochs=1)
    r = model.evaluate(x_test, y_test)
    print("Performance:", r[0])


if __name__ == "__main__":
    models = [get_model_a(), get_model_b()]
    for i in range(30):
        for m in models:
            evaluate(m, i)
