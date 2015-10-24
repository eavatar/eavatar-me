
console.log(Backbone)

var hash = window.location.hash;

if(hash && hash.startsWith('#')) {
    hash = hash.substring(1)
}
console.log("hashtag:" + hash)

if(hash == 'token') {
    window.location.hash = '';
}