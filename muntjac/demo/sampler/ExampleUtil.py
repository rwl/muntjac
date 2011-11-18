
from random import random

from babel.numbers import format_currency
from muntjac.util import defaultLocale

from muntjac.data.util.indexed_container import IndexedContainer
from muntjac.data.util.hierarchical_container import HierarchicalContainer

from muntjac.terminal.resource import IResource
from muntjac.terminal.theme_resource import ThemeResource

from babel import Locale


class ExampleUtil(object):

    lorem = '. '.join(['Romani ite domum' for _ in range(300)])

#    lorem = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut ut "
#            "massa eget erat dapibus sollicitudin. Vestibulum ante ipsum "
#            "primis in faucibus orci luctus et ultrices posuere cubilia "
#            "Curae; Pellentesque a augue. Praesent non elit. Duis sapien "
#            "dolor, cursus eget, pulvinar eget, eleifend a, est. Integer in "
#            "nunc. Vivamus consequat ipsum id sapien. Duis eu elit vel "
#            "libero posuere luctus. Aliquam ac turpis. Aenean vitae justo "
#            "in sem iaculis pulvinar. Cum sociis natoque penatibus et "
#            "magnis dis parturient montes, nascetur ridiculus mus. Aliquam "
#            "sit amet mi. "
#            "<br/>"
#            "Aenean auctor, mi sit amet ultricies pulvinar, dui urna "
#            "adipiscing odio, ut faucibus odio mauris eget justo. Mauris "
#            "quis magna quis augue interdum porttitor. Sed interdum, tortor "
#            "laoreet tincidunt ullamcorper, metus velit hendrerit nunc, id "
#            "laoreet mauris arcu vitae est. Nulla nec nisl. Mauris orci "
#            "nibh, tempor nec, sollicitudin ac, venenatis sed, lorem. "
#            "Quisque dignissim tempus erat. Maecenas molestie, pede ac "
#            "ultrices interdum, felis neque vulputate quam, in sodales felis "
#            "odio quis mi. Aliquam massa pede, pharetra quis, tincidunt "
#            "quis, fringilla at, mauris. Vestibulum a massa. Vestibulum "
#            "luctus odio ut quam. Maecenas congue convallis diam. Cras urna "
#            "arcu, vestibulum vitae, blandit ut, laoreet id, risus. Ut "
#            "condimentum, arcu sit amet placerat blandit, augue nibh "
#            "pretium nunc, in tempus sem dolor non leo. Etiam fringilla "
#            "mauris a odio. Nunc lorem diam, interdum eget, lacinia in, "
#            "scelerisque sit amet, purus. Nam ornare. "
#            "<br/>"
#            "Donec placerat dui ut orci. Phasellus quis lacus at nisl "
#            "elementum cursus. Cras bibendum egestas nulla. Phasellus "
#            "pulvinar ullamcorper odio. Etiam ipsum. Proin tincidunt. "
#            "Aliquam aliquet. Etiam purus odio, commodo sed, feugiat "
#            "volutpat, scelerisque molestie, velit. Aenean sed sem sit "
#            "amet libero sodales ultrices. Donec dictum, arcu sed iaculis "
#            "porttitor, est mauris pulvinar purus, sit amet porta purus "
#            "neque in risus. Mauris libero. Maecenas rhoncus. Morbi "
#            "quis nisl. "
#            "<br/>"
#            "Vestibulum laoreet tortor eu elit. Cras euismod nulla eu "
#            "sapien. Sed imperdiet. Maecenas vel sapien. Nulla at purus eu "
#            "diam auctor lobortis. Donec pede eros, lacinia tincidunt, "
#            "tempus eu, molestie nec, velit. Nullam ipsum odio, euismod "
#            "non, aliquet nec, consequat ac, felis. Duis fermentum mauris "
#            "sed justo. Suspendisse potenti. Praesent at libero sit amet "
#            "ipsum imperdiet fermentum. Aliquam enim nisl, dictum id, "
#            "lacinia sit amet, elementum posuere, ipsum. Integer luctus "
#            "dictum libero. Pellentesque sed pede sed nisl bibendum "
#            "porttitor. Phasellus tempor interdum nisi. Mauris nec magna. "
#            "Phasellus massa pede, vehicula sed, ornare at, ullamcorper ut, "
#            "nisl. Sed turpis nisl, hendrerit sit amet, consequat id, "
#            "auctor nec, arcu. Quisque fringilla tincidunt massa. In "
#            "eleifend, nulla sed mollis vestibulum, mauris orci facilisis "
#            "ante, id pharetra dolor ipsum vitae sem. Integer dictum. "
#            "<br/>"
#            "Nunc ut odio. Lorem ipsum dolor sit amet, consectetur "
#            "adipiscing elit. Donec mauris tellus, dapibus vel, hendrerit "
#            "vel, sollicitudin ut, ligula. Ut justo metus, accumsan "
#            "placerat, ultrices sit amet, congue at, nulla. Integer in "
#            "quam. Cras sollicitudin mattis magna. Vestibulum neque eros, "
#            "egestas ut, tincidunt vel, ullamcorper non, ligula. Vivamus "
#            "eu lacus. Donec rhoncus metus et odio. Donec est. Nulla "
#            "facilisi. Suspendisse potenti. Etiam tempor pede nec ante. "
#            "Vestibulum adipiscing velit vel neque. "
#            "<br/>"
#            "Quisque ornare erat rhoncus lectus. Donec vitae ante at enim "
#            "mollis egestas. Mauris convallis. Fusce convallis, nisl eu "
#            "sagittis suscipit, risus ligula aliquam libero, in imperdiet "
#            "neque mi non risus. Aenean dictum ultricies risus. Praesent ut "
#            "ligula vitae purus ornare auctor. Cras tellus mauris, "
#            "adipiscing ac, dignissim auctor, faucibus in, sem. Cras mauris "
#            "libero, pharetra sit amet, lacinia eu, vehicula eleifend, "
#            "sapien. Donec ac tellus. Sed eros dui, vulputate vel, auctor "
#            "pharetra, tincidunt at, ipsum. Duis at dolor ac leo condimentum "
#            "pulvinar. Donec molestie, dolor et fringilla elementum, nibh "
#            "nibh iaculis orci, eu elementum odio turpis et odio. Phasellus "
#            "fermentum, justo id placerat egestas, arcu nunc molestie ante, "
#            "non imperdiet ligula lectus sed erat. Quisque sed ligula. Sed "
#            "ac nulla. Nullam massa. "
#            "<br/>"
#            "Sed a purus. Mauris non nibh blandit neque cursus scelerisque. "
#            "Quisque ultrices sem nec dolor. Donec non diam ut dui consequat "
#            "venenatis. Nullam risus massa, egestas in, facilisis tristique, "
#            "molestie sed, mi. Duis euismod turpis sit amet quam. Vestibulum "
#            "ornare felis eget dolor. Phasellus ac urna vel sapien lacinia "
#            "adipiscing. Donec egestas felis id mi. Sed erat. Vestibulum "
#            "porta vulputate neque. Maecenas scelerisque, sem id sodales "
#            "pretium, sem mauris rhoncus magna, at scelerisque tortor mauris "
#            "nec dui. Nullam blandit rhoncus velit. Nam accumsan, enim id "
#            "vestibulum feugiat, lorem nibh placerat urna, eget laoreet diam "
#            "tortor at lorem. Suspendisse imperdiet consectetur dolor. ")

    iso3166 = ["AFGHANISTAN", "AF",
            "ALAND ISLANDS", "AX", "ALBANIA", "AL", "ALGERIA", "DZ",
            "AMERICAN SAMOA", "AS", "ANDORRA", "AD", "ANGOLA", "AO",
            "ANGUILLA", "AI", "ANTARCTICA", "AQ", "ANTIGUA AND BARBUDA", "AG",
            "ARGENTINA", "AR", "ARMENIA", "AM", "ARUBA", "AW", "AUSTRALIA",
            "AU", "AUSTRIA", "AT", "AZERBAIJAN", "AZ", "BAHAMAS", "BS",
            "BAHRAIN", "BH", "BANGLADESH", "BD", "BARBADOS", "BB", "BELARUS",
            "BY", "BELGIUM", "BE", "BELIZE", "BZ", "BENIN", "BJ", "BERMUDA",
            "BM", "BHUTAN", "BT", "BOLIVIA", "BO", "BOSNIA AND HERZEGOVINA",
            "BA", "BOTSWANA", "BW", "BOUVET ISLAND", "BV", "BRAZIL", "BR",
            "BRITISH INDIAN OCEAN TERRITORY", "IO", "BRUNEI DARUSSALAM", "BN",
            "BULGARIA", "BG", "BURKINA FASO", "BF", "BURUNDI", "BI",
            "CAMBODIA", "KH", "CAMEROON", "CM", "CANADA", "CA", "CAPE VERDE",
            "CV", "CAYMAN ISLANDS", "KY", "CENTRAL AFRICAN REPUBLIC", "CF",
            "CHAD", "TD", "CHILE", "CL", "CHINA", "CN", "CHRISTMAS ISLAND",
            "CX", "COCOS (KEELING) ISLANDS", "CC", "COLOMBIA", "CO", "COMOROS",
            "KM", "CONGO", "CG", "CONGO, THE DEMOCRATIC REPUBLIC OF THE", "CD",
            "COOK ISLANDS", "CK", "COSTA RICA", "CR", "COTE D'IVOIRE", "CI",
            "CROATIA", "HR", "CUBA", "CU", "CYPRUS", "CY", "CZECH REPUBLIC",
            "CZ", "DENMARK", "DK", "DJIBOUTI", "DJ", "DOMINICA", "DM",
            "DOMINICAN REPUBLIC", "DO", "ECUADOR", "EC", "EGYPT", "EG",
            "EL SALVADOR", "SV", "EQUATORIAL GUINEA", "GQ", "ERITREA", "ER",
            "ESTONIA", "EE", "ETHIOPIA", "ET", "FALKLAND ISLANDS (MALVINAS)",
            "FK", "FAROE ISLANDS", "FO", "FIJI", "FJ", "FINLAND", "FI",
            "FRANCE", "FR", "FRENCH GUIANA", "GF", "FRENCH POLYNESIA", "PF",
            "FRENCH SOUTHERN TERRITORIES", "TF", "GABON", "GA", "GAMBIA", "GM",
            "GEORGIA", "GE", "GERMANY", "DE", "GHANA", "GH", "GIBRALTAR", "GI",
            "GREECE", "GR", "GREENLAND", "GL", "GRENADA", "GD", "GUADELOUPE",
            "GP", "GUAM", "GU", "GUATEMALA", "GT", "GUERNSEY", "GG", "GUINEA",
            "GN", "GUINEA-BISSAU", "GW", "GUYANA", "GY", "HAITI", "HT",
            "HEARD ISLAND AND MCDONALD ISLANDS", "HM",
            "HOLY SEE (VATICAN CITY STATE)", "VA", "HONDURAS", "HN",
            "HONG KONG", "HK", "HUNGARY", "HU", "ICELAND", "IS", "INDIA", "IN",
            "INDONESIA", "ID", "IRAN, ISLAMIC REPUBLIC OF", "IR", "IRAQ", "IQ",
            "IRELAND", "IE", "ISLE OF MAN", "IM", "ISRAEL", "IL", "ITALY",
            "IT", "JAMAICA", "JM", "JAPAN", "JP", "JERSEY", "JE", "JORDAN",
            "JO", "KAZAKHSTAN", "KZ", "KENYA", "KE", "KIRIBATI", "KI",
            "KOREA, DEMOCRATIC PEOPLE'S REPUBLIC OF", "KP",
            "KOREA, REPUBLIC OF", "KR", "KUWAIT", "KW", "KYRGYZSTAN", "KG",
            "LAO PEOPLE'S DEMOCRATIC REPUBLIC", "LA", "LATVIA", "LV",
            "LEBANON", "LB", "LESOTHO", "LS", "LIBERIA", "LR",
            "LIBYAN ARAB JAMAHIRIYA", "LY", "LIECHTENSTEIN", "LI", "LITHUANIA",
            "LT", "LUXEMBOURG", "LU", "MACAO", "MO",
            "MACEDONIA, THE FORMER YUGOSLAV REPUBLIC OF", "MK", "MADAGASCAR",
            "MG", "MALAWI", "MW", "MALAYSIA", "MY", "MALDIVES", "MV", "MALI",
            "ML", "MALTA", "MT", "MARSHALL ISLANDS", "MH", "MARTINIQUE", "MQ",
            "MAURITANIA", "MR", "MAURITIUS", "MU", "MAYOTTE", "YT", "MEXICO",
            "MX", "MICRONESIA, FEDERATED STATES OF", "FM",
            "MOLDOVA, REPUBLIC OF", "MD", "MONACO", "MC", "MONGOLIA", "MN",
            "MONTENEGRO", "ME", "MONTSERRAT", "MS", "MOROCCO", "MA",
            "MOZAMBIQUE", "MZ", "MYANMAR", "MM", "NAMIBIA", "NA", "NAURU",
            "NR", "NEPAL", "NP", "NETHERLANDS", "NL", "NETHERLANDS ANTILLES",
            "AN", "NEW CALEDONIA", "NC", "NEW ZEALAND", "NZ", "NICARAGUA",
            "NI", "NIGER", "NE", "NIGERIA", "NG", "NIUE", "NU",
            "NORFOLK ISLAND", "NF", "NORTHERN MARIANA ISLANDS", "MP", "NORWAY",
            "NO", "OMAN", "OM", "PAKISTAN", "PK", "PALAU", "PW",
            "PALESTINIAN TERRITORY, OCCUPIED", "PS", "PANAMA", "PA",
            "PAPUA NEW GUINEA", "PG", "PARAGUAY", "PY", "PERU", "PE",
            "PHILIPPINES", "PH", "PITCAIRN", "PN", "POLAND", "PL", "PORTUGAL",
            "PT", "PUERTO RICO", "PR", "QATAR", "QA", "REUNION", "RE",
            "ROMANIA", "RO", "RUSSIAN FEDERATION", "RU", "RWANDA", "RW",
            "SAINT BARTHELEMY", "BL", "SAINT HELENA", "SH",
            "SAINT KITTS AND NEVIS", "KN", "SAINT LUCIA", "LC", "SAINT MARTIN",
            "MF", "SAINT PIERRE AND MIQUELON", "PM",
            "SAINT VINCENT AND THE GRENADINES", "VC", "SAMOA", "WS",
            "SAN MARINO", "SM", "SAO TOME AND PRINCIPE", "ST", "SAUDI ARABIA",
            "SA", "SENEGAL", "SN", "SERBIA", "RS", "SEYCHELLES", "SC",
            "SIERRA LEONE", "SL", "SINGAPORE", "SG", "SLOVAKIA", "SK",
            "SLOVENIA", "SI", "SOLOMON ISLANDS", "SB", "SOMALIA", "SO",
            "SOUTH AFRICA", "ZA",
            "SOUTH GEORGIA AND THE SOUTH SANDWICH ISLANDS", "GS", "SPAIN",
            "ES", "SRI LANKA", "LK", "SUDAN", "SD", "SURINAME", "SR",
            "SVALBARD AND JAN MAYEN", "SJ", "SWAZILAND", "SZ", "SWEDEN", "SE",
            "SWITZERLAND", "CH", "SYRIAN ARAB REPUBLIC", "SY",
            "TAIWAN, PROVINCE OF CHINA", "TW", "TAJIKISTAN", "TJ",
            "TANZANIA, UNITED REPUBLIC OF", "TZ", "THAILAND", "TH",
            "TIMOR-LESTE", "TL", "TOGO", "TG", "TOKELAU", "TK", "TONGA", "TO",
            "TRINIDAD AND TOBAGO", "TT", "TUNISIA", "TN", "TURKEY", "TR",
            "TURKMENISTAN", "TM", "TURKS AND CAICOS ISLANDS", "TC", "TUVALU",
            "TV", "UGANDA", "UG", "UKRAINE", "UA", "UNITED ARAB EMIRATES",
            "AE", "UNITED KINGDOM", "GB", "UNITED STATES", "US",
            "UNITED STATES MINOR OUTLYING ISLANDS", "UM", "URUGUAY", "UY",
            "UZBEKISTAN", "UZ", "VANUATU", "VU", "VENEZUELA", "VE", "VIET NAM",
            "VN", "VIRGIN ISLANDS, BRITISH", "VG", "VIRGIN ISLANDS, U.S.",
            "VI", "WALLIS AND FUTUNA", "WF", "WESTERN SAHARA", "EH", "YEMEN",
            "YE", "ZAMBIA", "ZM", "ZIMBABWE", "ZW"]

    iso3166_PROPERTY_NAME = 'name'
    iso3166_PROPERTY_SHORT = 'short'
    iso3166_PROPERTY_FLAG = 'flag'
    hw_PROPERTY_NAME = 'name'
    hw_PROPERTY_ICON = 'icon'

    locale_PROPERTY_LOCALE = 'locale'
    locale_PROPERTY_NAME = 'name'
    _locales = [['fi', 'FI', 'Finnish'], ['de', 'DE', 'German'], ['en', 'US',
            'US - English'], ['sv', 'SE', 'Swedish']]
    _hardware = [['Desktops', 'Dell OptiPlex GX240', 'Dell OptiPlex GX260',
            'Dell OptiPlex GX280'], ['Monitors', 'Benq T190HD', 'Benq T220HD',
            'Benq T240HD'], ['Laptops', 'IBM ThinkPad T40', 'IBM ThinkPad T43',
            'IBM ThinkPad T60']]

    PERSON_PROPERTY_FIRSTNAME = 'First Name'
    PERSON_PROPERTY_LASTNAME = 'Last Name'
    PERSON_PROPERTY_NAME = 'Name'
    _firstnames = ['John', 'Mary', 'Joe', 'Sarah', 'Jeff', 'Jane', 'Peter',
            'Marc', 'Robert', 'Paula', 'Lenny', 'Kenny', 'Nathan', 'Nicole',
            'Laura', 'Jos', 'Josie', 'Linus']
    _lastnames = ['Torvalds', 'Smith', 'Adams', 'Black', 'Wilson', 'Richards',
            'Thompson', 'McGoff', 'Halas', 'Jones', 'Beck', 'Sheridan',
            'Picard', 'Hill', 'Fielding', 'Einstein']

    ORDER_DESCRIPTION_PROPERTY_ID = 'description'
    ORDER_QUANTITY_PROPERTY_ID = 'quantity'
    ORDER_UNITPRICE_PROPERTY_ID = 'unitprice'
    ORDER_ITEMPRICE_PROPERTY_ID = 'itemprice'


    @classmethod
    def getPersonContainer(cls):
        contactContainer = IndexedContainer()
        contactContainer.addContainerProperty(cls.PERSON_PROPERTY_FIRSTNAME,
                str, '')
        contactContainer.addContainerProperty(cls.PERSON_PROPERTY_LASTNAME,
                str, '')
        i = 0
        while i < 50:
            fn = cls._firstnames[int(random() * len(cls._firstnames))]
            ln = cls._lastnames[int(random() * len(cls._lastnames))]
            idd = fn + ln
            item = contactContainer.addItem(idd)
            if item is not None:
                i += 1
                item.getItemProperty(cls.PERSON_PROPERTY_FIRSTNAME).setValue(fn)
                item.getItemProperty(cls.PERSON_PROPERTY_LASTNAME).setValue(ln)
        return contactContainer


    @classmethod
    def getNameContainer(cls):
        contactContainer = IndexedContainer()
        contactContainer.addContainerProperty(cls.PERSON_PROPERTY_NAME, str, '')
        i = 0
        while i < 50:
            fn = cls._firstnames[int(random() * len(cls._firstnames))]
            ln = cls._lastnames[int(random() * len(cls._lastnames))]
            idd = fn + ln
            item = contactContainer.addItem(idd)
            if item is not None:
                i += 1
                v = fn + ' ' + ln
                item.getItemProperty(cls.PERSON_PROPERTY_NAME).setValue(v)
        return contactContainer


    @classmethod
    def getLocaleContainer(cls):
        localeContainer = IndexedContainer()
        localeContainer.addContainerProperty(cls.locale_PROPERTY_LOCALE,
                Locale, None)
        localeContainer.addContainerProperty(cls.locale_PROPERTY_NAME,
                str, None)
        for i in range(len(cls._locales)):
            idd = cls._locales[i][2]
            item = localeContainer.addItem(idd)
            v = Locale(cls._locales[i][0], cls._locales[i][1])
            item.getItemProperty(cls.locale_PROPERTY_LOCALE).setValue(v)
            v = cls._locales[i][2]
            item.getItemProperty(cls.locale_PROPERTY_NAME).setValue(v)
        return localeContainer


    @classmethod
    def getStaticISO3166Container(cls):
        return cls.getISO3166Container()


    @classmethod
    def getISO3166Container(cls):
        c = IndexedContainer()
        cls.fillIso3166Container(c)
        return c


    @classmethod
    def fillIso3166Container(cls, container):
        container.addContainerProperty(cls.iso3166_PROPERTY_NAME, str, None)
        container.addContainerProperty(cls.iso3166_PROPERTY_SHORT, str, None)
        container.addContainerProperty(cls.iso3166_PROPERTY_FLAG, IResource, None)
        i = 0
        while i < len(cls.iso3166):
            name = cls.iso3166[i]
            i += 1
            idd = cls.iso3166[i]
            item = container.addItem(idd)
            item.getItemProperty(cls.iso3166_PROPERTY_NAME).setValue(name)
            item.getItemProperty(cls.iso3166_PROPERTY_SHORT).setValue(idd)
            v = ThemeResource('../sampler/flags/' + idd.lower() + '.gif')
            item.getItemProperty(cls.iso3166_PROPERTY_FLAG).setValue(v)
            i += 1
        container.sort([cls.iso3166_PROPERTY_NAME], [True])


    @classmethod
    def getHardwareContainer(cls):
        item = None
        itemId = 0  # Increasing numbering for itemId:s

        # Create new container
        hwContainer = HierarchicalContainer()
        # Create containerproperty for name
        hwContainer.addContainerProperty(cls.hw_PROPERTY_NAME, str, None)
        # Create containerproperty for icon
        hwContainer.addContainerProperty(cls.hw_PROPERTY_ICON, ThemeResource,
                ThemeResource('../runo/icons/16/document.png'))

        for i in range(len(cls._hardware)):
            # Add new item
            item = hwContainer.addItem(itemId)

            # Add name property for item
            v = cls._hardware[i][0]
            item.getItemProperty(cls.hw_PROPERTY_NAME).setValue(v)

            # Allow children
            hwContainer.setChildrenAllowed(itemId, True)

            itemId += 1
            for j in range(1, len(cls._hardware[i])):
                if j == 1:
                    v = ThemeResource('../runo/icons/16/folder.png')
                    item.getItemProperty(cls.hw_PROPERTY_ICON).setValue(v)

                # Add child items
                item = hwContainer.addItem(itemId)
                v = cls._hardware[i][j]
                item.getItemProperty(cls.hw_PROPERTY_NAME).setValue(v)
                hwContainer.setParent(itemId, itemId - j)
                hwContainer.setChildrenAllowed(itemId, False)

                itemId += 1

        return hwContainer


    @classmethod
    def fillContainerWithEmailAddresses(cls, c, amount):
        for _ in range(amount):
            break  # TODO


    @classmethod
    def getOrderContainer(cls):
        container = IndexedContainer()

        # Create the container properties
        container.addContainerProperty(cls.ORDER_DESCRIPTION_PROPERTY_ID,
                str, '')
        container.addContainerProperty(cls.ORDER_QUANTITY_PROPERTY_ID,
                int, 0)
        container.addContainerProperty(cls.ORDER_UNITPRICE_PROPERTY_ID,
                str, '$0')
        container.addContainerProperty(cls.ORDER_ITEMPRICE_PROPERTY_ID,
                str, '$0')

        # Create some orders
        cls.addOrderToContainer(container, 'Domain Name', 3, 7.99)
        cls.addOrderToContainer(container, 'SSL Certificate', 1, 119.0)
        cls.addOrderToContainer(container, 'Web Hosting', 1, 19.95)
        cls.addOrderToContainer(container, 'Email Box', 20, 0.15)
        cls.addOrderToContainer(container, 'E-Commerce Setup', 1, 25.0)
        cls.addOrderToContainer(container, 'Technical Support', 1, 50.0)

        return container


    @classmethod
    def addOrderToContainer(cls, container, description, quantity, price):
        l = defaultLocale()
        itemId = container.addItem()
        item = container.getItem(itemId)

        v = description
        item.getItemProperty(cls.ORDER_DESCRIPTION_PROPERTY_ID).setValue(v)

        v = quantity
        item.getItemProperty(cls.ORDER_QUANTITY_PROPERTY_ID).setValue(v)

        v = format_currency(price, currency='USD', locale=l).encode('utf-8')
        item.getItemProperty(cls.ORDER_UNITPRICE_PROPERTY_ID).setValue(v)

        v = format_currency(price * quantity, currency='USD', locale=l)
        v = v.encode('utf-8')
        item.getItemProperty(cls.ORDER_ITEMPRICE_PROPERTY_ID).setValue(v)
