# aws-ec2-workshop
EC2 portion of Codebase AWS Workshop

## Creating EC2 Instance

1. Launch Instance -> Ubuntu 14.04 -> t2.micro -> Review and Launch
2. Edit security groups -> Select an existing group -> default -> Review and Launch
3. Launch -> Create a new key pair -> aws-workshop -> Download Key Pair -> Launch Instances

## Connecting to EC2

If you're on Windows, follow [instructions here](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/putty.html).

If you're on Mac/Linux,

```
cd [path/to/pem-file-directory]
mv aws-workshop.pem.txt aws-workshop.pem
chmod 400 aws-workshop.pem
ssh -i aws-workshop.pem ubuntu@[ec2-dns]
```

## Install Stuff

```
sudo apt-get update
sudo apt-get install apache2 libapache2-mod-wsgi git python-pip python-dev
sudo pip install --upgrade pip
```

## Fork This Repository

```
git clone [your repo url]
cd aws-ec2-workshop/workshop/ec2
sudo pip install -r requirements.txt
sudo ln -sT ~/aws-ec2-workshop/workshop/ec2/flaskapp /var/www/html/flaskapp
sudo cp 000-default.conf /etc/apache2/sites-enabled/000-default.conf
sudo apachectl restart
```

## Train Model

```
cd flaskapp
mkdir model
python train.py
sudo apachectl restart
```

## Modify Web Client

1. Open `workshop/client/js/main.js`
2. Replace URL with EC2 DNS, add `http://` to the front.
3. Open `workshop/client/index.html`, draw something!

## Build a Multilayer Convolutional Network

TensorFlow tutorial: https://www.tensorflow.org/get_started/mnist/pros

Changes to `workshop/ec2/flaskapp/flaskapp.py`:
```
classifier = cv.load_conv(sess, '/var/www/html/flaskapp/model_conv/model.ckpt')
```

Push to EC2:
```
git commit -a -m 'Add deep convolutional network'
git push origin master
```

On EC2:
```
git pull origin master
sudo apachectl restart
```

Now run `index.html` locally again, recognition should be more accurate!
