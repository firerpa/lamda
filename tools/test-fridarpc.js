Java.perform(function() {
        var String = Java.use("java.lang.String")
        rpc.exports = {
                getMyString: function (paramA, paramB) {
                        return performRpcJVMCall(function() {
                                // 可以使用 Frida java 相关功能，Java.use 等
                                var newParam = String.$new("helloWorld").toString()
                                return newParam + ":" + paramA + paramB
                        })
                },
                getMyString1: function (paramA, paramB) {
                        return performRpcJVMCallOnMain(function() {
                                // 可以使用 Frida java 相关功能，Java.use 等
                                // 执行于应用的主进程，适用于涉及到 UI 主线程相关的功能
                                var newParam = String.$new("helloWorld").toString()
                                return newParam + ":" + paramA + paramB
                        })
                },
                getMyString2: function (paramA, paramB) {
                        return performRpcCall(function() {
                                // 这里不能使用 Java 相关功能
                                return paramA + paramB
                        })
                },
        }
// 创建名为 myRpcName 的调用接口
createRpcEndpoint("myRpcName", rpc.exports)
console.log("fridarpc test loaded")
});
