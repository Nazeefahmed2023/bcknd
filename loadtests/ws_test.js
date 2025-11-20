import ws from "k6/ws";
import { check, sleep } from "k6";


export let options = {
vus: 50,
duration: '1m',
};


export default function () {
const token = __ENV.WS_TOKEN || 'TEST_TOKEN';
const url = `ws://localhost:8000/ws/delivery/location/?token=${token}`;


const res = ws.connect(url, null, function (socket) {
socket.on('open', function() {
socket.send(JSON.stringify({ type: 'location', order_id: 1, lat: 12.9716, lng: 77.5946 }));
socket.setInterval(function() {
socket.send(JSON.stringify({ type: 'location', order_id: 1, lat: 12.9716 + Math.random()/100, lng: 77.5946 + Math.random()/100 }));
}, 1000);
});


socket.on('message', function(msg) {
check(msg, { 'msg received': m => m.length > 0 });
});


socket.setTimeout(function() {
socket.close();
}, 30000);
});


check(res, { 'connected': r => r && r.status === 101 });
sleep(1);
}