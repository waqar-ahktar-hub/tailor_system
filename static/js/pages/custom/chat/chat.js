"use strict";

// Class definition
var KTAppChat = function () {
    var chatAsideEl;
    var chatContentEl;

    // Private functions
    var initAside = function () {
        // Mobile offcanvas for mobile mode
        var offcanvas = new KTOffcanvas(chatAsideEl, {
            overlay: true,
            baseClass: 'kt-app__aside',
            closeBy: 'kt_chat_aside_close',
            toggleBy: 'kt_chat_aside_mobile_toggle'
        });

        // User listing
        var userListEl = KTUtil.find(chatAsideEl, '.kt-scroll');
        if (!userListEl) {
            return;
        }

        // Initialize perfect scrollbar
        KTUtil.scrollInit(userListEl, {
            mobileNativeScroll: true,
            desktopNativeScroll: false,
            resetHeightOnDestroy: true,
            handleWindowResize: true,
            rememberPosition: true,
            height: function() {
                var height;
                var portletBodyEl = KTUtil.find(chatAsideEl, '.kt-portlet > .kt-portlet__body');
                var widgetEl = KTUtil.find(chatAsideEl, '.kt-widget.kt-widget--users');
                var searchbarEl = KTUtil.find(chatAsideEl, '.kt-searchbar');

                if (KTUtil.isInResponsiveRange('desktop')) {
                    height = KTLayout.getContentHeight();
                } else {
                    height = KTUtil.getViewPort().height;
                }

                if (chatAsideEl) {
                    height = height - parseInt(KTUtil.css(chatAsideEl, 'margin-top')) - parseInt(KTUtil.css(chatAsideEl, 'margin-bottom'));
                    height = height - parseInt(KTUtil.css(chatAsideEl, 'padding-top')) - parseInt(KTUtil.css(chatAsideEl, 'padding-bottom'));
                }

                if (widgetEl) {
                    height = height - parseInt(KTUtil.css(widgetEl, 'margin-top')) - parseInt(KTUtil.css(widgetEl, 'margin-bottom'));
                    height = height - parseInt(KTUtil.css(widgetEl, 'padding-top')) - parseInt(KTUtil.css(widgetEl, 'padding-bottom'));
                }

                if (portletBodyEl) {
                    height = height - parseInt(KTUtil.css(portletBodyEl, 'margin-top')) - parseInt(KTUtil.css(portletBodyEl, 'margin-bottom'));
                    height = height - parseInt(KTUtil.css(portletBodyEl, 'padding-top')) - parseInt(KTUtil.css(portletBodyEl, 'padding-bottom'));
                }

                if (searchbarEl) {
                    height = height - parseInt(KTUtil.css(searchbarEl, 'height'));
                    height = height - parseInt(KTUtil.css(searchbarEl, 'margin-top')) - parseInt(KTUtil.css(searchbarEl, 'margin-bottom'));
                }

                height = height - 5;

                return height;
            }
        });
    };

    return {
        init: function() {
            chatAsideEl = KTUtil.getByID('kt_chat_aside');
            initAside();
            KTChat.setup(KTUtil.getByID('kt_chat_content'));

            if (KTUtil.getByID('kt_app_chat_launch_btn')) {
                setTimeout(function() {
                    KTUtil.getByID('kt_app_chat_launch_btn').click();
                }, 1000);
            }
        }
    };
}();

KTUtil.ready(function() {
    KTAppChat.init();
});
