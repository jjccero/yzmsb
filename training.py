from t_init import *
import random

IMAGE_PATH = 'images/'
VAILD_PATH = 'vaild/'


def get_namelist():
    NAME_LIST = []
    VAILD_LIST = []
    for e in os.listdir(IMAGE_PATH):
        NAME_LIST.append(e[:CAPTCHA_LEN])
    for e in os.listdir(VAILD_PATH):
        VAILD_LIST.append(e[:CAPTCHA_LEN])
    random.shuffle(NAME_LIST)
    random.shuffle(VAILD_LIST)
    return NAME_LIST, VAILD_LIST


NAME_LIST, VAILD_LIST = get_namelist()


def name2vec(name):
    vec = zeros(CAPTCHA_LEN * CHAR_SET_LEN)
    for i, c in enumerate(name):
        c = ord(c)
        if c > 57:
            c = c - 87
        else:
            c = c - 48
        vec[i * CHAR_SET_LEN + c] = 1
    return vec


def vec2text(vec):
    char_pos = vec.nonzero()[0]
    text = ''
    for c in char_pos:
        char_idx = c % CHAR_SET_LEN
        if char_idx < 10:
            text += chr(48 + char_idx)
        elif char_idx < 36:
            text += chr(87 + char_idx)
        else:
            raise ValueError('error')
    return text


def get_data_and_label(name, path, type='.jpg'):
    img = Image.open(path + name + type)
    # 转为灰度图
    img = img.convert("L")
    image_array = array(img)[:IMAGE_HEIGHT, :IMAGE_WIDTH]
    x = image_array.flatten() / 255
    y = name2vec(name)
    return x, y


def get_next_batch(batch_size, step, path, list):
    batch_x = zeros([batch_size, IMAGE_HEIGHT * IMAGE_WIDTH])
    batch_y = zeros([batch_size, CAPTCHA_LEN * CHAR_SET_LEN])
    indexStart = step * batch_size
    for i in range(batch_size):
        index = (i + indexStart) % len(list)
        name = list[index]
        img_x, img_y = get_data_and_label(name, path)
        batch_x[i, :] = img_x
        batch_y[i, :] = img_y
    return batch_x, batch_y

MODELS_PATH='models/jjcero_txtSecretCode.model'

def train_crack_captcha_cnn():
    output = crack_captcha_cnn()
    loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(labels=Y, logits=output))
    optimizer = tf.train.AdamOptimizer(learning_rate=0.0001).minimize(loss)

    predict = tf.reshape(output, [-1, CAPTCHA_LEN, CHAR_SET_LEN])
    max_idx_p = tf.argmax(predict, 2)
    max_idx_l = tf.argmax(tf.reshape(Y, [-1, CAPTCHA_LEN, CHAR_SET_LEN]), 2)
    correct_pred = tf.equal(max_idx_p, max_idx_l)
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

    saver = tf.train.Saver()
    with tf.Session() as sess:
        saver.restore(sess, MODELS_PATH)
        #sess.run(tf.global_variables_initializer())


        for step in range(10000):
            batch_x, batch_y = get_next_batch(64, step, IMAGE_PATH, NAME_LIST)
            _, loss_ = sess.run([optimizer, loss], feed_dict={X: batch_x, Y: batch_y, keep_prob: 0.8})
            step += 1
            if step % 100 == 0:
                batch_x_test, batch_y_test = get_next_batch(64, step, VAILD_PATH, VAILD_LIST)
                acc,loss_ = sess.run([accuracy,loss], feed_dict={X: batch_x_test, Y: batch_y_test, keep_prob: 1.})
                print(step, acc,loss_)
                if acc > 0.99:
                    break
        saver.save(sess, MODELS_PATH)
        sess.close()


train_crack_captcha_cnn()
