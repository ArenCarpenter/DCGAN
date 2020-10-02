import numpy as np
import argparse
import mlflow.sklearn
from mlflow import log_metric
from keras import Sequential
from keras.layers import Dense, Dropout
from time import time

# Generate dummy data
def gen_data(input_dim=20, bsize=10000) -> list:
    """
    Generate random data for model.
    :param input_dim: Dimensions for generated data.
    :param bsize: Batch size, how many observations to generate.
    :return: List of test/train objects.
    """
    x_train = np.random.random((bsize, input_dim))
    y_train = np.random.randint(2, size=(bsize, 1))
    x_test = np.random.random((int(bsize * 0.10), input_dim))
    y_test = np.random.randint(2, size=(int(bsize * 0.10), 1))

    return [x_train, y_train, x_test, y_test]

def build_model(in_dim=20, drate=0.5, out=64):
    """
    Generate Keras model with hyperparameters.
    :param in_dim: Size of input dimension.
    :param drate: Dropout rate.
    :param out: Output size.
    :return: Keras model.
    """
    mdl = Sequential()
    mdl.add(Dense(out, input_dim=in_dim, activation='relu'))
    if drate:
        mdl.add(Dropout(drate))
    mdl.add(Dense(out, activation='relu'))
    if drate:
        mdl.add(Dropout(drate))
    mdl.add(Dense(out, activation='relu'))
    if drate:
        mdl.add(Dropout(drate))
    mdl.add(Dense(1, activation='sigmoid'))

    return mdl

def compile_and_run_model(mdl, train_data, epochs=20, batch_size=128):
    """
    Compile and run Keras model generated from build_model().
    :param mdl: Model object generated from build_model().
    :param train_data: Training data.
    :param epochs: Training time.
    :param batch_size: Batch size.
    :return: List of Accuracy and Loss.
    """
    mdl.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

    mdl.fit(train_data[0], train_data[1],
          epochs=epochs,
          batch_size=bs,
          verbose=1)

    score = mdl.evaluate(train_data[2], train_data[3], batch_size=batch_size)
    print('Test loss:', score[0])
    print('Test accuracy:', score[1])

    print("Predictions for Y:")
    print(mdl.predict(train_data[2][:5]))
    mdl.summary()

    return ([score[0], score[1]])

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--drop_rate", help="Drop rate", nargs='?', action='store', default=0.5, type=float)
    parser.add_argument("--input_dim", help="Input dimension for the network.", action='store', nargs='?', default=20, type=int)
    parser.add_argument("--bs", help="Number of rows or size of the tensor", action='store', nargs='?', default=10000, type=int)
    parser.add_argument("--output", help="Output from First & Hidden Layers", action='store',  nargs='?', default=64, type=int)
    parser.add_argument("--train_batch_size", help="Training Batch Size", nargs='?', action='store', default=64, type=int)
    parser.add_argument("--epochs", help="Number of epochs for training", nargs='?', action='store', default=30, type=int)

    args = parser.parse_args()

    drop_rate = args.drop_rate
    input_dim = args.input_dim
    bs = args.bs
    output = args.output
    epochs = args.epochs
    batch_size = args.train_batch_size

    print("drop_rate", args.drop_rate)
    print("input_dim", args.input_dim)
    print("size", args.bs)
    print("output", args.output)
    print("train_batch_size", args.train_batch_size)
    print("epochs", args.epochs)

    data = gen_data(input_dim=args.input_dim, bsize=args.train_batch_size)
    model = build_model(in_dim=args.input_dim, drate=args.drop_rate, out=args.output)

    start_time = time()
    with mlflow.start_run():
        results = compile_and_run_model(model, data, epochs=epochs, batch_size=batch_size)
        mlflow.log_param("drop_rate", args.drop_rate)
        mlflow.log_param("input_dim", args.input_dim)
        mlflow.log_param("size", args.bs)
        mlflow.log_param("output", args.output)
        mlflow.log_param("train_batch_size", args.train_batch_size)
        mlflow.log_param("epochs", args.epochs)
        mlflow.log_param("loss", results[0])
        mlflow.log_param("acc", results[1])

    timed = time() - start_time

    print("This model took", timed, "seconds to train and test.")
    log_metric("Time to run", timed)