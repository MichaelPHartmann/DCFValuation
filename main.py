import dcf
import pickle
import os

SAVE_FOLDER = ".saves"

def save(object, name):
    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER, exist_ok=True)
    path = os.path.join(SAVE_FOLDER, name + ".pickle")
    with open(path, "wb") as f:
        pickle.dump(object, f)


def load(name):
    path = os.path.join(SAVE_FOLDER, name + ".pickle")
    if os.path.exists(path):
        with open(path, "rb") as f:
            return pickle.load(f)
    else:
        print("'{}' does not exist".format(path))


'''
This will run the DCF based on new data
'''
def run_new(symbol, cr):
    data = dcf.DCF_Data(symbol)
    save(data, symbol)
    print(dcf.compute_dcf(data, cr))


'''
This will run the DCF and only request more data iff it's not already saved
'''
def run_cache(symbol, cr):
    data = load(symbol)
    if not data:
        data = dcf.DCF_Data(symbol)
        save(data, symbol)
    print(dcf.compute_dcf(data, cr))


'''
This will only run the DCF iff the data already exists
'''
def run_test(symbol, cr):
    data = load(symbol)
    if not data:
        return
    print(dcf.compute_dcf(data, cr))


if __name__ == "__main__":
    run("AAPL", 'baa2')
