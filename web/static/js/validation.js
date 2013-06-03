/**
 * Created with PyCharm.
 * User: eamonnmaguire
 * Date: 03/06/2013
 * Time: 14:00
 * To change this template use File | Settings | File Templates.
 */
function validateSearchInput() {
    var searchValue = document.forms["search"]["search-text"].value;
    console.log('Search value is ' + searchValue)
    return searchValue != "";
}