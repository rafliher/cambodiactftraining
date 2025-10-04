Java.perform(function() {
    let mainActivity = Java.use("com.example.clickme.MainActivity");
    
    mainActivity.getFlagButtonClick.implementation = function(view) {
        this.CLICKS.value = 99999999
        let ret = this.getFlagButtonClick(view);
        return ret;
    };
}, 0);