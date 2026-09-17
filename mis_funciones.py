import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix


def plot_confusion_matrix(y, y_predict):
    """Dibuja y devuelve la matriz de confusión usando solo matplotlib."""
    cm = confusion_matrix(y, y_predict)
    fig, ax = plt.subplots()
    im = ax.imshow(cm, cmap='Blues')
    ax.set_title('Matriz de confusión')
    ax.set_xlabel('Predicciones')
    ax.set_ylabel('Etiquetas reales')
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(['no aterrizó', 'aterrizó'])
    ax.set_yticklabels(['no aterrizó', 'aterrizó'])

    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, str(cm[i, j]), ha='center', va='center', color='white' if cm[i, j] > cm.max() / 2 else 'black')

    fig.colorbar(im, ax=ax)
    plt.show()
    return cm
