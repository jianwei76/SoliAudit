import os
import joblib

def predict_vul(data, algo, vul):

    if vul not in {'Underflow', 'Overflow'}:
        data = get_reduced_data(data)

    model = load_model(algo, vul)
    if model is None:
        return None

    y = model.predict(data)[0]
    print("%s: %s" % (vul, y))
    return y


def __model_dump_path(algo, vuln):
    return ".model/%s/%s.pkl" % (algo, vuln)

def save_model(algo, vuln, model):
    path = __model_dump_path(algo, vuln)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(model, path)

def load_model(algo, vuln):
    path = __model_dump_path(algo, vuln)
    if not os.path.exists(path):
        return None
    return joblib.load(path)

if __name__ == '__main__':
    model = load_model('logistic', 'Overflow')

    dir = '../sc-src'
    for f in os.listdir(dir):
        if not f.endswith('.sol'):
            continue
        f = os.path.join(dir, f)
        predict_vul(data, 'logistic', 'Overflow')

