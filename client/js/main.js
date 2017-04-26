/* global $ */
class Main {
    constructor() {
        this.canvas = document.getElementById('main');
        this.input = document.getElementById('input');
        this.canvas.width  = 448; // 16 * 28 + 1
        this.canvas.height = 448; // 16 * 28 + 1
        this.ctx = this.canvas.getContext('2d');
        this.canvas.addEventListener('mousedown', this.onMouseDown.bind(this));
        this.canvas.addEventListener('mouseup',   this.onMouseUp.bind(this));
        this.canvas.addEventListener('mousemove', this.onMouseMove.bind(this));
        this.initialize();
    }
    initialize() {
        this.ctx.fillStyle = '#FFFFFF';
        this.ctx.fillRect(0, 0, 448, 448);
        this.drawInput();
        $('#output td').text('').removeClass('success');
    }
    onMouseDown(e) {
        this.canvas.style.cursor = 'default';
        this.drawing = true;
        this.prev = this.getPosition(e.clientX, e.clientY);
    }
    onMouseUp() {
        this.drawing = false;
        this.drawInput();
    }
    onMouseMove(e) {
        if (this.drawing) {
            var curr = this.getPosition(e.clientX, e.clientY);
            this.ctx.lineWidth = 32;
            this.ctx.lineCap = 'round';
            this.ctx.beginPath();
            this.ctx.moveTo(this.prev.x, this.prev.y);
            this.ctx.lineTo(curr.x, curr.y);
            this.ctx.stroke();
            this.ctx.closePath();
            this.prev = curr;
        }
    }
    getPosition(clientX, clientY) {
        var rect = this.canvas.getBoundingClientRect();
        return {
            x: clientX - rect.left,
            y: clientY - rect.top
        };
    }
    drawInput() {
        var ctx = this.input.getContext('2d');
        var img = new Image();
        img.onload = () => {
            var inputs = [];
            var small = document.createElement('canvas').getContext('2d');
            small.drawImage(img, 0, 0, img.width, img.height, 0, 0, 28, 28);
            var data = small.getImageData(0, 0, 28, 28).data;
            for (var i = 0; i < 28; i++) {
                for (var j = 0; j < 28; j++) {
                    var n = 4 * (i * 28 + j);
                    inputs[i * 28 + j] = (data[n + 0] + data[n + 1] + data[n + 2]) / 3;
                    ctx.fillStyle = 'rgb(' + [data[n + 0], data[n + 1], data[n + 2]].join(',') + ')';
                    ctx.fillRect(j * 5, i * 5, 5, 5);
                }
            }
            if (Math.min(...inputs) === 255) {
                return;
            }
            inputs = inputs.map(function(i) {
                return (255 - i) / 255;
            });



            // var hidden_canvas = document.createElement('canvas');
            // hidden_canvas.width = img.width;
            // hidden_canvas.height = img.height;
            // var hidden_context = hidden_canvas.getContext('2d');
            // hidden_context.drawImage(img, 0, 0);
            // var data = hidden_context.getImageData(0, 0, img.width, img.height).data;
            
            // var gray = [];
            // for (var i=0; i<448; i++) {
            //     for (var j=0; j<448; j++) {
            //         var n = 4 * (i * 448 + j);
            //         gray[i * 448 + j] = (data[n] + data[n+1] + data[n+2]) / 3;
            //     }
            // }
            
            // var inputs2 = [];
            // for (var row=0; row<28; row++) {
            //     for (var col=0; col<28; col++) {
            //         var sum = 0;
            //         for (var i=16*row; i<16*(row+1); i++) {
            //             for (var j=16*col; j<16*(col+1);j++) {
            //                 sum += gray[i*448+j];
            //             }
            //         }
            //         sum /= 256;
            //         inputs2[row*28+col] = sum;
            //     }
            // }

            // if (Math.min(...inputs2) === 255) {
            //     return;
            // }
            // inputs2 = inputs2.map(function(i) {
            //     return (255 - i) / 255;
            // });

            $.ajax({
                url: 'http://localhost:5000/classify',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(inputs),
                success: (data) => {
                    $('#output').html(data)
                }
            });

            // $.ajax({
            //     url: 'http://localhost:5000/classify',
            //     method: 'POST',
            //     contentType: 'application/json',
            //     data: JSON.stringify(inputs2),
            //     success: (data) => {
            //         console.log('inputs2: ' + data)

            //     }
            // });
        };
        img.src = this.canvas.toDataURL();
    }
}

$(() => {
    var main = new Main();
    $('#clear').click(() => {
        main.initialize();
    });
});
