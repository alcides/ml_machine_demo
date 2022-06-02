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
    return model.evaluate(x_test, y_test)


if __name__ == "__main__": 
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-s", "--seed", dest="seed", type="int")
    parser.add_option("-m", "--model", dest="model", type="int")

    (options, args) = parser.parse_args()

    models = [get_model_a(), get_model_b()]
    seed = options.seed
    model = models[options.model]
    v = evaluate(model, seed)
    print(seed, ";", options.model, ";", ";".join([ str(x) for x in v ]))
