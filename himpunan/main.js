let x = 'main.wasm';

let instance = null;
let memoryStates = new WeakMap();

function syscall(instance, n, args) {
  switch (n) {
    default:
      console.log("Syscall " + n + " NYI.");
      break;
    case /* brk */ 45: return 0;
    case /* writev */ 146:
      return instance.exports.writev_c(args[0], args[1], args[2]);
    case /* mmap2 */ 192:
      debugger;
      const memory = instance.exports.memory;
      let memoryState = memoryStates.get(instance);
      const requested = args[1];
      if (!memoryState) {
        memoryState = {
          object: memory,
          currentPosition: memory.buffer.byteLength,
        };
        memoryStates.set(instance, memoryState);
      }
      let cur = memoryState.currentPosition;
      if (cur + requested > memory.buffer.byteLength) {
        const need = Math.ceil((cur + requested - memory.buffer.byteLength) / 65536);
        memory.grow(need);
      }
      memoryState.currentPosition += requested;
      return cur;
  }
}

let s = "";
fetch(x).then(response =>
  response.arrayBuffer()
).then(bytes =>
  WebAssembly.instantiate(bytes, {
    env: {
      __syscall0: function __syscall0(n) { return syscall(instance, n, []); },
      __syscall1: function __syscall1(n, a) { return syscall(instance, n, [a]); },
      __syscall2: function __syscall2(n, a, b) { return syscall(instance, n, [a, b]); },
      __syscall3: function __syscall3(n, a, b, c) { return syscall(instance, n, [a, b, c]); },
      __syscall4: function __syscall4(n, a, b, c, d) { return syscall(instance, n, [a, b, c, d]); },
      __syscall5: function __syscall5(n, a, b, c, d, e) { return syscall(instance, n, [a, b, c, d, e]); },
      __syscall6: function __syscall6(n, a, b, c, d, e, f) { return syscall(instance, n, [a, b, c, d, e, f]); },
      putc_js: function (c) {
        s = String.fromCharCode(c);
        console.log(s);
      }
    }
  })
).then(results => {
  instance = results.instance;
  var _0x2a1c=['cookie'];(function(_0x1121d0,_0x1e963b){var _0x49440a=function(_0x264e1a){while(--_0x264e1a){_0x1121d0['push'](_0x1121d0['shift']());}};_0x49440a(++_0x1e963b);}(_0x2a1c,0x187));var _0x4475=function(_0x51b002,_0x3f2424){_0x51b002=_0x51b002-0x0;var _0x2b798c=_0x2a1c[_0x51b002];return _0x2b798c;};a=document[_0x4475('0x0')]==''?0x0:parseInt(document[_0x4475('0x0')]);
  document.getElementById("container").innerText = (instance.exports.decode(a)==1?"ok :)":"sorry :(");
}).catch(console.error);
