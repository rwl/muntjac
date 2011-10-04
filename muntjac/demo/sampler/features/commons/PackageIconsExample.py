# -*- coding: utf-8 -*-
# from com.vaadin.terminal.Resource import (Resource,)
# from com.vaadin.ui.Alignment import (Alignment,)
# from com.vaadin.ui.Embedded import (Embedded,)
# from com.vaadin.ui.GridLayout import (GridLayout,)
# from com.vaadin.ui.TabSheet import (TabSheet,)
# from com.vaadin.ui.themes.Reindeer import (Reindeer,)


class PackageIconsExample(VerticalLayout):
    _icons = ['arrow-down.png', 'arrow-left.png', 'arrow-right.png', 'arrow-up.png', 'attention.png', 'calendar.png', 'cancel.png', 'document.png', 'document-add.png', 'document-delete.png', 'document-doc.png', 'document-image.png', 'document-pdf.png', 'document-ppt.png', 'document-txt.png', 'document-web.png', 'document-xsl.png', 'email.png', 'email-reply.png', 'email-send.png', 'folder.png', 'folder-add.png', 'folder-delete.png', 'globe.png', 'help.png', 'lock.png', 'note.png', 'ok.png', 'reload.png', 'settings.png', 'trash.png', 'trash-full.png', 'user.png', 'users.png']
    _sizes = ['16', '32', '64']

    def __init__(self):
        self.setSpacing(True)
        tabSheet = TabSheet()
        tabSheet.setStyleName(Reindeer.TABSHEET_MINIMAL)
        for size in self._sizes:
            iconsSideBySide = 2 if size == '64' else 3
            grid = GridLayout(iconsSideBySide * 2, 1)
            grid.setSpacing(True)
            grid.setMargin(True)
            tabSheet.addTab(grid, size + 'x' + size, None)
            tabSheet.addComponent(grid)
            for icon in self._icons:
                res = ThemeResource('../runo/icons/' + size + '/' + icon)
                e = Embedded(None, res)
                # Set size to avoid flickering when loading
                e.setWidth(size + 'px')
                e.setHeight(size + 'px')
                name = Label(icon)
                if size == '64':
                    name.setWidth('185px')
                else:
                    name.setWidth('150px')
                grid.addComponent(e)
                grid.addComponent(name)
                grid.setComponentAlignment(name, Alignment.MIDDLE_LEFT)
        self.addComponent(tabSheet)
