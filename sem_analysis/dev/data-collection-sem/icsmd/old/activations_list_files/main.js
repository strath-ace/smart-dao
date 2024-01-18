

function Lightbox() {

    /**
     *
     * @type {HTMLElement} lightbox
     */
    this.lightbox = null;

    /**
     *
     * @type {HTMLElement} lightboxContent
     */
    this.lightboxContent = null;


    this.init();
}

Lightbox.prototype.init = function () {
    if (!this.lightbox) {
        this.lightbox = this.buildLightbox();
        this.lightboxContent = this.lightbox.querySelector('.lightbox-content');
        this.lightbox.querySelector('.lightbox-close').addEventListener('click', this.hide.bind(this));
    }
}

Lightbox.prototype.buildLightbox = function () {

    var lightbox = document.createElement('div');
    lightbox.classList.add('lightbox', 'media-lightbox');

    var lightboxContent = document.createElement('div');
    lightboxContent.classList.add('lightbox-content');

    var lightboxCloseButton = document.createElement('button');
    lightboxCloseButton.classList.add('lightbox-close');
    lightboxCloseButton.appendChild(getTimesIcon());
    lightboxCloseButton.setAttribute('title', '\u0043\u006c\u006f\u0073\u0065');

    lightbox.append(lightboxCloseButton, lightboxContent);

    return document.body.appendChild(lightbox);
}

/**
 *
 * @param {HTMLImageElement} image
 */
Lightbox.prototype.show = function (imageURL) {
    var imageElement = document.createElement('img');
    imageElement.src = imageURL;
    this.lightboxContent.appendChild(imageElement);
    this.lightbox.classList.add('active');
    document.body.classList.add('no-scroll');
}

Lightbox.prototype.hide = function () {
    this.lightbox.classList.remove('active');
    document.body.classList.remove('no-scroll');
    this.clear();
}

Lightbox.prototype.clear = function () {
    if (this.lightboxContent.childElementCount) {
        this.lightboxContent.removeChild(this.lightboxContent.firstChild);
    }
}

function createSVGIcon(iconName) {
    var svgElement = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svgElement.classList.add('icon', iconName);
    var useElement = document.createElementNS('http://www.w3.org/2000/svg', 'use')
    useElement.setAttributeNS('http://www.w3.org/1999/xlink', 'href', '#' + iconName);

    svgElement.appendChild(useElement);
    return svgElement;
}

function getTimesIcon() {
    return createSVGIcon('icon-cross');
}

function onImageLoadingError(element, placeholderUrl) {
    element.src = placeholderUrl;
    element.setAttribute('data-placeholder', '');
}

function fetchMedia(offset, count, type = null) {
    var url = new URL(document.location.origin + '/charter-portlets/cpi-mvc/media_library');
    var searchParams = url.searchParams;
    searchParams.set('offset', offset);
    searchParams.set('count', count);
    if (type) {
        searchParams.set('tag', type);
    }
    var headers = new Headers();
    headers.set('Accept-Language', locale);
    return fetch(url.toString(), {
        headers: headers
    });
}

function fetchMediaLibraryFilters() {
    var url = document.location.origin + '/charter-portlets/cpi-mvc/media_library/filters';
    var headers = new Headers();
    headers.set('Accept-Language', locale);
    return fetch(url, {
        headers: headers
    });
}

function fetchDocumentLibraryMediaTypes() {
    var url = document.location.origin + '/charter-portlets/cpi-mvc/library/media/types';
    var headers = new Headers();
    headers.set('Accept-Language', locale);
    return fetch(url, { headers: headers }).then(response => response.json());
}

function fillMediaLibraryMediaTypeFilter(mediaTypes, filtersDropdown) {
    Object.keys(mediaTypes).forEach(mediaType => {
        var optionElement = document.createElement('option');
        optionElement.innerText = mediaTypes[mediaType];
        optionElement.value = mediaType;
        filtersDropdown.appendChild(optionElement);
    })
}

function fillDocumentLibraryTypeFilter(types, filtersDropdown) {
    Object.keys(types).forEach(type => {
        var optionElement = document.createElement('option');
        optionElement.innerText = types[type];
        optionElement.value = type;
        filtersDropdown.appendChild(optionElement);
    })
}

/**
 * Updates media library filters dropdown with fetched filters.
 * @param {HTMLElement} filtersDropdown
 */
function updateFiltersDropdown(filtersDropdown) {
    fetchMediaLibraryFilters()
        .then(response => response.json())
        .then(data => {
            fillMediaLibraryMediaTypeFilter(data.mediaTypes, filtersDropdown);
        });
}

/**
 * Updates document library filters dropdown with fetched filters.
 * @param {HTMLElement} filtersDropdown
 */
function getDocumentLibraryFiltersDropdown(filtersDropdown) {
    fetchDocumentLibraryMediaTypes()
        .then(data => fillDocumentLibraryTypeFilter(data, filtersDropdown))
}

/**
 * Creates media item element.
 * @param item
 * @returns {HTMLDivElement}
 */
function createMediaItem(item) {
    var cardElement = document.createElement('div');
    cardElement.classList.add('card-item', 'media-item', 'item');
    cardElement.id = 'media-item-' + item.id;

    var cardItemPicture = document.createElement('picture');
    cardItemPicture.classList.add('media-item-picture', 'item-picture');

    if(item.image) {
        cardElement.setAttribute('data-image-url', item.image);
        cardItemPicture.classList.add('link');
    }

    var cardItemImage = document.createElement('img');
    cardItemImage.classList.add('media-item-thumbnail');
    cardItemImage.addEventListener('error', function (event) {
        this.src = '/charter-theme/images/placeholders/media.png';
        this.setAttribute('data-placeholder', '');
    }, { once: true });
    cardItemImage.src = item.thumbnail;
    cardItemImage.alt = '';

    var contentWrapper = document.createElement('div');
    contentWrapper.classList.add('con-wrap');
    var title = document.createElement('h3');
    title.classList.add('mb-2');
    title.innerText = item.title;

    var description = document.createElement('p');
    description.innerHTML = item.description;

    var copyright = document.createElement('p');
    copyright.classList.add('credit');
    copyright.innerHTML = item.copyright;

    cardItemPicture.appendChild(cardItemImage);
    contentWrapper.append(title, description, copyright);
    cardElement.append(cardItemPicture, contentWrapper);
    return cardElement;
}

/**
 * Creates document library media item element.
 * @param item
 * @returns {HTMLDivElement}
 */
function createDocumentLibraryItem(item) {

    var previewExcludedFileExtensions = ['zip', 'doc', 'docx', 'txt', 'xls', 'xlsx'];

    var cardElement = document.createElement('div');
    cardElement.classList.add('card-item', 'document-library-item', 'media-item', 'item');
    cardElement.id = 'document-library-item-' + item.id;

    var cardItemPicture = document.createElement('picture');
    cardItemPicture.classList.add('media-item-picture', 'item-picture');

    if(item.image) {
        cardElement.setAttribute('data-image-url', item.image);
        cardItemPicture.classList.add('link');
    }

    var cardItemImage = document.createElement('img');
    cardItemImage.classList.add('media-item-thumbnail');
    cardItemImage.addEventListener('error', function (event) {
        this.src = '/charter-theme/images/placeholders/documents.png';
        this.setAttribute('data-placeholder', '');
    }, { once: true });
    cardItemImage.src = item.previewUrl;
    cardItemImage.alt = '';

    cardItemPicture.appendChild(cardItemImage);

    var contentWrapper = document.createElement('div');
    contentWrapper.classList.add('con-wrap');
    var title = document.createElement('h3');
    title.classList.add('mb-2');
    title.innerText = item.title;

    var description = document.createElement('p');
    description.innerHTML = item.description;

    var actionButtonsContainer = document.createElement('div');
    actionButtonsContainer.classList.add('action-buttons');

    var showPreviewButton = !previewExcludedFileExtensions.filter(function(extension) {
        return item.docUrl.indexOf('.' + extension) !== -1;
    }).length;

    if(showPreviewButton) {
        var previewPDFButton = document.createElement('button');
        previewPDFButton.classList.add('preview-pdf-btn', 'btn', 'action-btn');
        previewPDFButton.setAttribute('data-href', item.docUrl);
        previewPDFButton.setAttribute('data-action', 'preview');
        previewPDFButton.setAttribute('title', '\u0050\u0072\u0065\u0076\u0069\u0065\u0077\u0020\u0050\u0044\u0046');

        var screenReaderTextElement = document.createElement('span');
        screenReaderTextElement.classList.add('sr-only');
        screenReaderTextElement.innerText = '\u0050\u0072\u0065\u0076\u0069\u0065\u0077\u0020\u0050\u0044\u0046';
        previewPDFButton.append(screenReaderTextElement);
        actionButtonsContainer.append(previewPDFButton);

        var imagePreviewPdfButton = previewPDFButton.cloneNode();
        imagePreviewPdfButton.classList.remove('action-btn');
        imagePreviewPdfButton.classList.add('btn', 'btn-link');
        imagePreviewPdfButton.append(cardItemPicture);
        cardElement.append(imagePreviewPdfButton);
    } else {
        cardElement.append(cardItemPicture);
    }

    var downloadPDFLink = document.createElement('a');
    downloadPDFLink.classList.add('action-btn', 'download-btn', 'btn');
    downloadPDFLink.href = item.docUrl;
    downloadPDFLink.setAttribute('download', '');
    downloadPDFLink.setAttribute('title', '\u0044\u006f\u0077\u006e\u006c\u006f\u0061\u0064\u0020\u0066\u0069\u006c\u0065');
    actionButtonsContainer.append(downloadPDFLink);
    contentWrapper.append(title, description, actionButtonsContainer);
    cardElement.append(contentWrapper);
    return cardElement;
}

/**
 *
 * @param {Array<object>} items
 * @param {HTMLElement} mediaContainer
 */
function addMediaItems(items, mediaContainer) {
    items
        .forEach(item => {
            var element = createMediaItem(item);
            mediaContainer.appendChild(element)
        });
}

/**
 *
 * @param {Array<object>} items
 * @param {HTMLElement} container
 */
function addDocumentLibraryItems(items, container) {
    items
        .forEach(item => {
            var element = createDocumentLibraryItem(item);
            container.appendChild(element)
        });
}

function removeChildren(element) {
    if(!element) {
        return;
    }
    while (element.childNodes.length) {
        element.removeChild(element.firstChild);
    }
}

function showNewsSection() {
    createNewsSearchHtmlStructure();

    var newsItemsContainer = document.querySelector('.news-events');
    var newsLoaderElement = document.querySelector('.loader');
    var newsLoaderButton = document.querySelector('.load-more');
    var newsTagsSelect = document.querySelector('.news-select');

    var newsOffset = 0;
    var newsCounter = 6;
    var newsTag;

    var clearNewsItemsContainer = function() {
        while (newsItemsContainer.childNodes.length) {
            newsItemsContainer.removeChild(newsItemsContainer.firstChild);
        }
    }

    if (newsTagsSelect) {
        setSelectOptions(newsTagsSelect);
        newsTagsSelect.addEventListener('change', function(event) {
            newsOffset = 0;
            newsTag = event.target.value;
            clearNewsItemsContainer();
            loadNews();
        })
    }

    clearNewsItemsContainer();

    var loadNews = function() {
        disableNewsLoaderButton();
        showNewsLoader();
        getNews(newsOffset, newsCounter, newsTag)
            .then(response => response.json())
            .then(data => {
                newsOffset += data.news.length;
                addNewsItems(data.news, newsItemsContainer);
                hideNewsLoader();
                if (newsItemsContainer.childElementCount >= data.size) {
                    hideLoadMediaButton();
                    disableNewsLoaderButton();
                } else {
                    showLoadMediaButton();
                    enableNewsLoaderButton();
                }
            })
            .catch(error => {
                console.log(error);
            })
    }

    if(newsLoaderButton) {
        newsLoaderButton.addEventListener('click', loadNews);
    }

    function disableNewsLoaderButton() {
        newsLoaderButton.setAttribute('disabled', '');
    }

    function enableNewsLoaderButton() {
        newsLoaderButton.removeAttribute('disabled');
    }

    function hideLoadMediaButton() {
        newsLoaderButton.classList.add('d-none');
    }

    function showLoadMediaButton() {
        newsLoaderButton.classList.remove('d-none');
    }

    function showNewsLoader() {
        newsLoaderElement.style.display = 'block';
    }

    function hideNewsLoader() {
        newsLoaderElement.style.display = 'none';
    }

    loadNews();
}

function createNewsSearchHtmlStructure() {
    var searchWrapper = document.querySelector('.news-search');
    searchWrapper.innerText = '';

    var searchTitle = createNewElement('p', 'news-title', null, '\u004e\u0065\u0077\u0073\u0020\u0074\u0079\u0070\u0065');
    var selectWrapper = createNewElement('span', 'news-select-wrapper');
    var searchSelect = createNewElement('select', 'news-select', {id: 'news-select'});
    var defaultOption = createNewElement('option', null, {value: ''}, '\u0041\u006c\u006c');

    searchSelect.appendChild(defaultOption);
    selectWrapper.appendChild(searchSelect);
    searchWrapper.append(searchTitle, selectWrapper);
}

function setSelectOptions(selectElement) {
    getNewsTagsNames()
        .then(response => response.json())
        .then(data => {
                var {newsMediaTypes} = data;
                fillSearchSelects(newsMediaTypes, selectElement);
            });                  
}

function getNewsTagsNames() { 
    var url = document.location.origin + '/charter-portlets/cpi-mvc/news/media/filters';
    var headers = new Headers();
    headers.set('Accept-Language', locale);
    return fetch(url, {headers});
}

function fillSearchSelects(tags, searchElement) {
    Object.keys(tags).forEach(tag => {
        var optionElement = createNewElement('option', null, {value: tag}, tags[tag]);
        searchElement.appendChild(optionElement);
    });
}

function getNews(offset, count, tag) {
    var url = new URL(document.location.origin + '/charter-portlets/cpi-mvc/news/media');
    var searchParams = url.searchParams;
    searchParams.set('offset', offset);
    searchParams.set('count', count);
    if (tag) {
        searchParams.set('tag', tag);
    }
    var headers = new Headers();
    headers.set('Accept-Language', locale);
    return fetch(url.toString(), {headers});
}

function addNewsItems(newsList, newsContainer) {
    newsList
        .forEach(news => {
            var newsItem = createNewsItem(news);
            newsContainer.appendChild(newsItem)
        });
}

function createNewsItem(news) {
    var newsItemContainer = createNewElement('div', 'item');
    var itemLinkElement = createNewElement('a', null, {href: news.mediaUrl});
    var itemImgElement = createNewElement('img', null, {src: news.thumbnail, alt: ''});
    var itemDescriptionContainer = createNewElement('div', 'con-wrap');
    var itemDateElement = createNewElement('p', null, null, news.date);
    var itemTitleElement = createNewElement('h3');
    var itemTitleLinkElement = createNewElement('a', null, {href: news.mediaUrl}, news.title);

    itemLinkElement.appendChild(itemImgElement);
    itemTitleElement.appendChild(itemTitleLinkElement);
    itemDescriptionContainer.append(itemDateElement, itemTitleElement);
    newsItemContainer.append(itemLinkElement, itemDescriptionContainer);

    itemImgElement.addEventListener('error', function () {
        this.src = '/charter-theme/images/placeholders/documents.png';
        this.setAttribute('data-placeholder', '');
        this.removeAttribute('alt');
    }, { once: true });

    return newsItemContainer;
}

function createNewElement(elementType, className = null, attributes = null, textContent = null) {
    var element = document.createElement(elementType);
    if (className) {
        element.classList.add(className);
    }
    if (attributes) {
        Object.keys(attributes).forEach(key => element.setAttribute(key, attributes[key]));
    }
    if (textContent) {
        element.innerText = textContent;
    }
    return element;
}

function getMediaLibrary() {
    var availableMediaCounter = document.getElementById('available-media-counter');
    var mediaItemsContainer = document.querySelector('.media-items');
    var mediaLoaderIndicator = document.getElementById('loader-media');
    var loadMediaButton = document.getElementById('load-media');
    var mediaLibraryTypeDropdown = document.getElementById('media-type');

    var mediaOffset = 0;
    var mediaCounter = 6;
    var mediaType;

    var clearMediaItemsContainer = function () {
        while (mediaItemsContainer.childNodes.length) {
            mediaItemsContainer.removeChild(mediaItemsContainer.firstChild);
        }
    }

    if (mediaLibraryTypeDropdown) {
        updateFiltersDropdown(mediaLibraryTypeDropdown);
        mediaLibraryTypeDropdown.addEventListener('change', function (event) {
            mediaOffset = 0;
            mediaType = event.target.value;
            clearMediaItemsContainer();
            loadMediaHandler();
        })
    }

    var mediaLibraryLightbox = new Lightbox();

    clearMediaItemsContainer();

    mediaItemsContainer.addEventListener('click', function (event) {
        var cardItemElement = event.target.closest('.media-item');
        var imageURL = cardItemElement.getAttribute('data-image-url');
        if (!event.target.classList.contains('media-item-thumbnail') || !imageURL) {
            return;
        }

        mediaLibraryLightbox.show(imageURL);
    });

    var loadMediaHandler = function() {
        disableLoadMediaButton();
        showMediaLoader();
        fetchMedia(mediaOffset, mediaCounter, mediaType)
            .then(response => response.json())
            .then(data => {
                mediaOffset += data.media.length;
                availableMediaCounter.innerText = data.size;
                addMediaItems(data.media, mediaItemsContainer);
                hideMediaLoader();
                if (mediaItemsContainer.childElementCount >= data.size) {
                    hideLoadMediaButton();
                    disableLoadMediaButton();
                } else {
                    showLoadMediaButton();
                    enableLoadMediaButton();
                }
            })
            .catch(error => {
                console.log(error);
            })
    }

    if(loadMediaButton) {
        loadMediaButton.addEventListener('click', loadMediaHandler);
    }

    function showMediaLoader() {
        mediaLoaderIndicator.style.display = 'block';
    }

    function hideMediaLoader() {
        mediaLoaderIndicator.style.display = 'none';
    }

    function disableLoadMediaButton() {
        loadMediaButton.setAttribute('disabled', '');
    }

    function enableLoadMediaButton() {
        loadMediaButton.removeAttribute('disabled');
    }

    function hideLoadMediaButton() {
        loadMediaButton.classList.add('d-none');
    }

    function showLoadMediaButton() {
        loadMediaButton.classList.remove('d-none');
    }

    loadMediaHandler();
}

function getProductsSelects(optDisaster) {
    $.get(document.location.origin + '/charter-portlets/cpi-mvc/activations/filters', function (data, status) {
        var disasters = sortObject(data.disasters);
        var satellites = sortObject(data.satellites);

        for (var disaster in disasters) {
            if (disasters.hasOwnProperty(disaster)) {
                $("#disaster").append('<option value="' + disaster + '">' + disasters[disaster] + '</option>');
            }
        }
        if (optDisaster) {
            $("#disaster").val(optDisaster);
        }

        for (var satellite in satellites) {
            if (satellites.hasOwnProperty(satellite)) {
                $("#satellites").append('<option value="' + satellite + '">' + satellites[satellite] + '</option>');
            }
        }
        for (var region in data.regions) {
            if (data.regions.hasOwnProperty(region)) {
                $("#regions").append('<option class="region" value="' + region + '">' + region + '</option>');
                for (var i = 0; i < data.regions[region].length; i++) {
                    $("#regions").append('<option value="' + data.regions[region][i] + '">' + data.regions[region][i] + '</option>');
                }
            }
        }
    });
}

function getDox(offset, count, type = null) {
    var url = document.location.origin + '/charter-portlets/cpi-mvc/library/media?offset=' + offset + '&count=' + count;
    if(type) {
        url += '&type=' + encodeURIComponent(type)
    }
    $.get(url, function (data, status) {
        $("#loader-dox").hide();

        addDocumentLibraryItems(data.documents, $(".dox")[0]);
        var showLoadMoreButton = data.size > 0 && $(".dox").children().length < data.size;

        if(!showLoadMoreButton) {
            $loadDoxButton.hide();
        }
        documentLibraryItemsCounterElement.innerText = data.size;
    });
}

function getProducts(offset, count, changeSelect, optDisaster) {
    $("#loader-prod").fadeIn();
    var satellite = $('#satellites').val();
    var disaster = $("#disaster").val();
    if (!disaster && optDisaster) {
        disaster = optDisaster;
    }
    var region = $("#regions").val();
    if (window.location.href.indexOf("disaster-types") > -1) {
        disaster = document.location.href.substr(document.location.href.lastIndexOf('/') + 1);
        if (disaster == 'ocean-wave') {
            disaster = 'ocean_wave';
        }
        if (disaster == 'oil-spills') {
            disaster = 'oilspills';
        }
    }
    $.ajax({
        url: document.location.origin + '/charter-portlets/cpi-mvc/activations/media?offset=' + offset + '&count=' + mediaLoadCount + '&satellite=' + satellite + '&disaster=' + disaster + '&region=' + region,
        type: "GET",
        headers: {"Accept-Language": locale}
    }).done(function (data) {
        var newsString = '';
        for (var y = 0; y < data.media.length; y++) {
            var activationURL = data.media[y].activationURL
            var activationElement = activationURL
                ? '<div class="activation-link"><a class="activation-button" href="/web/guest/activations/-/article/' + activationURL + '">' + '\u0047\u006f\u0020\u0074\u006f\u0020\u0061\u0063\u0074\u0069\u0076\u0061\u0074\u0069\u006f\u006e' + ' <img class="arrow" src="/charter-theme/images/cos2/arr-black.png"></a></div>'
                : '';
            newsString += '<div class="item"><a href="' + data.media[y].image + '"><picture class="item-picture"><img src="' + data.media[y].thumbnail
                + '"></picture></a><div class="con-wrap"><h3>' + data.media[y].title + '</h3><p><a href="' + data.media[y].image
                + '">' + '\u0041\u0063\u0071\u0075\u0069\u0072\u0065\u0064' + ': ' + data.media[y].acquired + '<br>' + '\u0053\u006f\u0075\u0072\u0063\u0065' + ': ' + data.media[y].source + '</a></p><p class="credit">' + '\u0043\u006f\u0070\u0079\u0072\u0069\u0067\u0068\u0074' + ': ' + data.media[y].credit
                + '</p></div>' + activationElement + '</div>';
        }

        $('#products-available span').html(data.size);

        $("#loader-prod").hide();

        if (changeSelect) {
            $(".products").html(newsString);
        }
        else {
            var $newStringElement = $(newsString);

            $newStringElement.each(function() {
                $(this).find('img').one('error', function() {
                    onImageLoadingError(this, '/charter-theme/images/placeholders/products.png');
                })
            })
            $newStringElement.appendTo($(".products"));
        }
    });
}

// function setTrianglesLinks() {
//     $('.how-row').each(function (i) {
//         var innerHTML = $(this).find('h2 a').attr('href'),
//             anchor = $('<a class="triangle"></a>'),
//             textWrap = $(this).find('p');
//
//         anchor.attr("href", innerHTML);
//         anchor.insertAfter(textWrap)
//     });
// }


//
function setMapHeight() {
    setTimeout(function () {
        var isSafari = false;
        if (($(window).width() > 998) && jQuery('html').hasClass("safari")) {
            // console.log(navigator.userAgent);
            isSafari = true;
            // console.log("status after change is " + isSafari);
            // console.log(location.href.indexOf('home' > -1));
            // console.log(jQuery('.resize.map-link'));
            var disasterTypesHeight = jQuery('.disasters #column-4').height();
            var mapLinkHeight = disasterTypesHeight - 142 + "px";
            // console.log(mapLinkHeight);
            jQuery('.resize.map-link').css("height", mapLinkHeight);
            // console.log('timeout')
        }
    }, 5000);
}


$('document').on('load', function () {
    setTimeout(function () {
        if ((jQuery(window).width() > 998) && jQuery('html').hasClass("safari")) {
            var disasterTypesHeight = $('#column-4').height();
            var mapLinkHeight = disasterTypesHeight - 142 + "px";
            // console.log(mapLinkHeight);
            jQuery('.resize.map-link').css("height", mapLinkHeight);
            // console.log('on load')
        }
    }, 5000);
});


$(window).resize(function () {
    setMapHeight();
});

$('.closebt').click(function () {
    $('.mobnav').fadeOut();
});
$('.burger').click(function () {
    $('.mobnav').fadeIn();
});
$('#load-prod').click(function () {
    offsetProd += countProd;
    getProducts(offsetProd, countProd, false);
});
$('#load-dox').click(function () {
    offsetDox += countDox;
    getDox(offsetDox, countDox, documentLibraryType);
});
$('.dox').on('click', '.preview-pdf-btn', function () {
    var href = $(this).data('href');
    var $previewModal = $('#pdf-preview-modal');
    var $previewModalTitle = $previewModal.find('.modal-title');
    var $previewModalBody = $previewModal.find('.modal-body');
    var $loader = $('<div class="loader"></div>');
    $previewModalBody.append($loader);
    var $iframe = $('<iframe src="' + href + '"></iframe>');
    $previewModalBody.append($iframe);
    var modalTitle = $(this).closest('.dox-wrap').find('.link-label').text() || '';
    $previewModalTitle.text(modalTitle);
    $previewModal.modal('show');
    $previewModal.addClass('loading');

    var handleHiddenBsModalEvent = function () {
        $previewModalTitle.text('Modal title');
        $previewModalBody.empty();
    };
    var handleIframeLoadEvent = function () {
        $loader.remove();
        $previewModal.removeClass('loading');
    }
    $previewModal.one('hidden.bs.modal', handleHiddenBsModalEvent);
    $iframe.one('load', handleIframeLoadEvent);
});

var actQuery = '?p_p_id=charterActivationsFiltered_WAR_charterportlets&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=getActivations&p_p_cacheability=cacheLevelPage&p_p_col_id=column-1&p_p_col_count=1';
var offset = 0;
var count = 9;
var mediaLoadCount = 6;
if ($('.products').parents('.type-top').length) {
    var countProd = 2;
}
else {
    var countProd = mediaLoadCount;
}
var offsetProd = 0;
var offsetDox = 0;
var countDox = 6;
var $loadDoxButton = $('#load-dox');

/**
 *
 * @type {HTMLSelectElement}
 */
var documentLibraryTypeDropdown = document.getElementById('document-library-type');
var documentLibraryContainer = document.querySelector('.document-library');
var documentLibraryItemsCounterElement = document.getElementById('document-library-counter');
var documentLibraryType;
if (documentLibraryTypeDropdown) {
    documentLibraryType = documentLibraryTypeDropdown.value;
    documentLibraryTypeDropdown.addEventListener('change', function (event) {
        documentLibraryType = event.target.value;
        offsetDox = 0;
        removeChildren(documentLibraryContainer.querySelector('.dox'));
        $loadDoxButton.show();
        getDox(offsetDox, countDox, documentLibraryType);
    })
}

$(document).ready(function () {
    handleScrollTopVisibility();
    if (window.location.href.indexOf('/web/guest/home') == -1) {
        var optDisaster;
        if (window.location.href.indexOf('/web/guest/news') != -1) {
            showNewsSection();
        } else if (window.location.href.indexOf('/web/guest/library') != -1) {
            optDisaster = getUrlParameter('disaster');
            getProductsSelects(optDisaster);
            getProducts(offsetProd, countProd, false, optDisaster);
            getDox(offsetDox, countDox, documentLibraryType);
            getMediaLibrary();
            getDocumentLibraryFiltersDropdown(documentLibraryTypeDropdown);
            // getDocumentLibraryMedia();
        } else if (window.location.href.indexOf('disaster-types') != -1) {
            optDisaster = getUrlParameter('disaster');
            getProductsSelects(optDisaster);
            getProducts(offsetProd, countProd, false, optDisaster);
        } else if (window.location.href.indexOf('media') != -1) {
            getMediaLibrary();
        }
        // setTrianglesLinks();
        setMapHeight();
        setActivationPageTitle();
    }
});

var lang = $('html')[0].lang;
var langOpen = false;
$('#' + lang).css("display", "block").addClass("active");
$('#' + lang).click(function (e) {
    e.preventDefault();
    if (langOpen) {
        $('.language a').css("display", "none");
        $('#' + lang).css("display", "block");
        langOpen = false;
    } else {
        $(this).parent().prepend($(this));
        $('.language a').fadeIn();
        langOpen = true;
    }
});
$('#satellites, #disaster, #regions').change(function () {
    getProducts(0, 4, true);
});
$('.newsletter-registration-input-text').attr("placeholder", $('.newsletter-registration-input-text').attr("title"));
$('#disasterTypes, #regionCountries').change(function () {
    timeline();
});

var getUrlParameter = function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
};


// $.get(document.location.href + "?p_p_id=charterActivationsFiltered_WAR_charterportlets&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=getActivations&p_p_cacheability=cacheLevelPage&p_p_col_id=column-1&p_p_col_count=1&region=the carribbean", function(data, status){
//         console.dir("Data: " + data + "\nStatus: " + status);
//     });
function sortObject(obj) {
    return Object.keys(obj).sort().reduce(function (result, key) {
        result[key] = obj[key];
        return result;
    }, {});
}

$(window).on('load', $('.cc-link'), function () {
    $('.cc-link').attr('href', 'terms-conditions')
});

function setActivationPageTitle() {
    var href = window.location.href;
    if (href.indexOf("charter-activations") >= 0) {
        $('.page-title').css('margin-bottom', '-13px');
    } else {
        return false
    }
}

function loadBootstrapJavascript() {
    $('body').append('<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>');
}

var scrollTopBtn = document.getElementById('scroll-top');

function setScrollTopButtonVisibility(state) {
    var visibilityClassName = 'visible';
    if (state) {
        scrollTopBtn.classList.add(visibilityClassName)
        scrollTopBtn.removeAttribute('disabled');
    } else {
        scrollTopBtn.classList.remove(visibilityClassName);
        scrollTopBtn.setAttribute('disabled', '');
    }
    scrollTopBtn.setAttribute('aria-hidden', (!state).toString());
}

function scrollToTop() {
    var ANIMATION_DURATION = 250;
    $('html, body').animate({
        scrollTop: 0
    }, ANIMATION_DURATION);
}

function handleScrollTopVisibility() {
    var showScrollTopBtn = document.documentElement.scrollTop > 500;
    setScrollTopButtonVisibility(showScrollTopBtn);

}

function scrollEventHandler() {
    handleScrollTopVisibility()
}

function scrollTopBtnClickHandler() {
    scrollToTop();
}

document.addEventListener('scroll', scrollEventHandler);
scrollTopBtn.addEventListener('click', scrollTopBtnClickHandler)
