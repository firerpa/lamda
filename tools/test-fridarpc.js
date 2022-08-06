Java.perform(function() {
        var String = Java.use("java.lang.String")
        rpc.exports = {
                getMyString: function (paramA, paramB) {
                        return performRpcJVMCall(function() {
                                var newParam = String.$new("helloWorld").toString()
                                return newParam + ":" + paramA + paramB
                        })
                }
        }
createFridaRpc("myRpcName", rpc.exports)
console.log("fridarpc test loaded")
});
