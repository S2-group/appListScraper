const CREDENTIALS = {
	username : 'YOUR USERNAME',
	password : 'YOUR PWD'
}

const PAGES = {
	login : 'https://www.appannie.com/account/login/?_ref=header',
	ranking : 'https://www.appannie.com/apps/google-play/top-chart/?country=US&device=&date=2019-04-01&feed=Free&rank_sorting_type=rank&page_number=0&page_size=500&order_type=desc&order_by=sort_order&category='
}

const LOGIN_FORM = {
	username_field : "#email",
	password_field : "#password",
	submit_button : "#submit"
}

const RANKING_TABLE = {
	table : "#sub-container > div.main.storestats_wrapper.page_top > div.inner > div.frame.frame-ss > div > div > div > div > div:nth-child(2) > app-group-table-container > div > div.ng-isolate-scope > div > div.dashboard-table.fixed-columns-table-container.ng-scope > div:nth-child(3) > table > tbody"
}

const categories = [ 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 66, 67, 68, 69, 70, 71, 72, 73, 75, 2, 12, 13, 14]

const puppeteer = require('puppeteer');
const fs = require('fs');

function delay(timeout) {
  return new Promise((resolve) => {
    setTimeout(resolve, timeout);
  });
}

function getRandomArbitrary(min, max) {
    return Math.random() * (max - min) + min;
}

(async () => {
  // INIT BROWSER
  const browser = await puppeteer.launch({ headless: false});
  const page = await browser.newPage();
  page.setViewport({ width : 1024, height : 768 });
  
  // GO TO LOGIN PAGE AND FILL FORM
  await page.goto(PAGES.login);

  await page.click(LOGIN_FORM.username_field);
  await page.keyboard.type(CREDENTIALS.username);

  await page.click(LOGIN_FORM.password_field);
  await page.keyboard.type(CREDENTIALS.password);

  await page.click(LOGIN_FORM.submit_button);
  await page.waitForNavigation();

  for (i = 0; i < categories.length; i ++){
  // GO TO RANKING PAGE AND WAIT UNTIL IT LOADS
  	await page.goto(PAGES.ranking + categories[i]);
  	await delay(getRandomArbitrary(60000, 180000));

  	// SELECT TABLE
  	const table = await page.evaluate(() => document.querySelector('#sub-container > div.main.storestats_wrapper.page_top > div.inner > div.frame.frame-ss > div > div > div > div > div:nth-child(2) > app-group-table-container > div > div.ng-isolate-scope').outerHTML);
  	await fs.writeFile("pages/category" + categories[i] + ".html", table, function(err) {});
  	console.log("Scraped page " + (i + 1) + " of " + categories.length );
  }

  await browser.close();
})();