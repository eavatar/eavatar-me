var isDebug = process.env.DEBUG || false;
var browsers = [isDebug ? 'Firefox' : 'PhantomJS'];

module.exports = function(config) {
	var client_dir = '';

	config.set({
		basePath: '.',
		browsers: browsers,
		frameworks: ['jasmine'],
		files: [
			'../js/jquery.min.js',
			'../js/jquery.mobile.min.js',
			'../js/jquery.notify.min.js',
			'../js/lodash.min.js',
			'../js/backbone.min.js',
			'../js/app-config.js',
			'../js/app-models.js',
			'../js/app-views.js',
			'../js/app-router.js',

			'spec/*.js',
	    ],
	    autoWatch: true,
	    singleRun: true,
	    reporters: ['progress', 'html', 'junit'],
	    htmlReporter: {
            outputFile: 'reports/web-tests.html',
            // Optional
            pageTitle: 'Unit Tests',
            subPageTitle: 'Avame Project'
        },
        junitReporter: {
            outputDir: 'reports', // results will be saved as $outputDir/$browserName.xml
            outputFile: undefined, // if included, results will be saved as $outputDir/$browserName/$outputFile
            suite: '', // suite will become the package name attribute in xml testsuite element
            useBrowserName: true // add browser name to report and classes names
        },
	    plugins : [
	        'karma-phantomjs-launcher',
	        'karma-firefox-launcher',
	        'karma-jasmine',
	        'karma-htmlfile-reporter',
	        'karma-junit-reporter'
	    ]
  });
};