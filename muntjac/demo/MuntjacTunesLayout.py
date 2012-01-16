
from muntjac.api import Application

from muntjac.terminal.sizeable import ISizeable
from muntjac.terminal.theme_resource import ThemeResource

from muntjac.ui.window import Notification

from muntjac.api import \
    (Alignment, ComboBox, Embedded, HorizontalLayout, HorizontalSplitPanel,
     Label, NativeButton, NativeSelect, Slider, Table, VerticalLayout, Window)


class MuntjacTunesLayout(Application):
    """Sample application layout, similar (almost identical) to Apple iTunes.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    """

    def init(self):
        # We'll build the whole UI here, since the application will not
        # contain any logic. Otherwise it would be more practical to
        # separate parts of the UI into different classes and methods.

        # Main (browser) window, needed in all Muntjac applications
        rootLayout = VerticalLayout()
        root = Window('MuntjacTunes', rootLayout)

        # We'll attach the window to the browser view already here, so
        # we won't forget it later.
        self.setMainWindow(root)

        root.showNotification(('This is an example of how you can do layouts '
                'in Muntjac.<br/>It is not a working sound player.'),
                Notification.TYPE_HUMANIZED_MESSAGE)

        # Our root window contains one VerticalLayout, let's make
        # sure it's 100% sized, and remove unwanted margins
        rootLayout.setSizeFull()
        rootLayout.setMargin(False)

        # Top area, containing playback and volume controls, play status,
        # view modes and search
        top = HorizontalLayout()
        top.setWidth('100%')
        top.setMargin(False, True, False, True)  # Enable horizontal margins
        top.setSpacing(True)

        # Let's attach that one straight away too
        root.addComponent(top)

        # Create the placeholders for all the components in the top area
        playback = HorizontalLayout()
        volume = HorizontalLayout()
        status = HorizontalLayout()
        viewmodes = HorizontalLayout()
        search = ComboBox()

        # Add the components and align them properly
        top.addComponent(playback)
        top.addComponent(volume)
        top.addComponent(status)
        top.addComponent(viewmodes)
        top.addComponent(search)
        top.setComponentAlignment(playback, Alignment.MIDDLE_LEFT)
        top.setComponentAlignment(volume, Alignment.MIDDLE_LEFT)
        top.setComponentAlignment(status, Alignment.MIDDLE_CENTER)
        top.setComponentAlignment(viewmodes, Alignment.MIDDLE_LEFT)
        top.setComponentAlignment(search, Alignment.MIDDLE_LEFT)

        # We want our status area to expand if the user resizes the root
        # window, and we want it to accommodate as much space as there is
        # available. All other components in the top layout should stay fixed
        # sized, so we don't need to specify any expand ratios for them (they
        # will automatically revert to zero after the following line).
        top.setExpandRatio(status, 1.0)

        # Playback controls
        prev = NativeButton('Previous')
        play = NativeButton('Play/pause')
        nextt = NativeButton('Next')
        playback.addComponent(prev)
        playback.addComponent(play)
        playback.addComponent(nextt)
        # Set spacing between the buttons
        playback.setSpacing(True)

        # Volume controls
        mute = NativeButton('mute')
        vol = Slider()
        vol.setOrientation(Slider.ORIENTATION_HORIZONTAL)
        vol.setWidth('100px')
        maxx = NativeButton('max')
        volume.addComponent(mute)
        volume.addComponent(vol)
        volume.addComponent(maxx)

        # Status area
        status.setWidth('80%')
        status.setSpacing(True)

        toggleVisualization = NativeButton('Mode')
        timeFromStart = Label('0:00')

        # We'll need another layout to show currently playing track and
        # progress
        trackDetails = VerticalLayout()
        trackDetails.setWidth('100%')
        track = Label('Track Name')
        album = Label('Album Name - Artist')
        track.setWidth(None)
        album.setWidth(None)
        progress = Slider()
        progress.setOrientation(Slider.ORIENTATION_HORIZONTAL)
        progress.setWidth('100%')
        trackDetails.addComponent(track)
        trackDetails.addComponent(album)
        trackDetails.addComponent(progress)
        trackDetails.setComponentAlignment(track, Alignment.TOP_CENTER)
        trackDetails.setComponentAlignment(album, Alignment.TOP_CENTER)

        timeToEnd = Label('-4:46')
        jumpToTrack = NativeButton('Show')

        # Place all components to the status layout and align them properly
        status.addComponent(toggleVisualization)
        status.setComponentAlignment(toggleVisualization,
                Alignment.MIDDLE_LEFT)
        status.addComponent(timeFromStart)
        status.setComponentAlignment(timeFromStart, Alignment.BOTTOM_LEFT)
        status.addComponent(trackDetails)
        status.addComponent(timeToEnd)
        status.setComponentAlignment(timeToEnd, Alignment.BOTTOM_LEFT)
        status.addComponent(jumpToTrack)
        status.setComponentAlignment(jumpToTrack, Alignment.MIDDLE_LEFT)

        # Then remember to specify the expand ratio
        status.setExpandRatio(trackDetails, 1.0)

        # View mode buttons
        viewAsTable = NativeButton('Table')
        viewAsGrid = NativeButton('Grid')
        coverflow = NativeButton('Coverflow')
        viewmodes.addComponent(viewAsTable)
        viewmodes.addComponent(viewAsGrid)
        viewmodes.addComponent(coverflow)

        # That covers the top bar. Now let's move on to the sidebar
        # and track listing

        # We'll need one splitpanel to separate the sidebar and track listing
        bottom = HorizontalSplitPanel()
        root.addComponent(bottom)

        # The splitpanel is by default 100% x 100%, but we'll need to
        # adjust our main window layout to accommodate the height
        root.getContent().setExpandRatio(bottom, 1.0)

        # Give the sidebar less space than the listing
        bottom.setSplitPosition(200, ISizeable.UNITS_PIXELS)

        # Let's add some content to the sidebar
        # First, we need a layout to but all components in
        sidebar = VerticalLayout()
        sidebar.setSizeFull()
        bottom.setFirstComponent(sidebar)

        # Then we need some labels and buttons, and an album cover image The
        # labels and buttons go into their own vertical layout, since we want
        # the 'sidebar' layout to be expanding (cover image in the bottom).
        # VerticalLayout is by default 100% wide.
        selections = VerticalLayout()
        library = Label('Library')
        music = NativeButton('Music')
        music.setWidth('100%')

        store = Label('Store')
        muntjacTunesStore = NativeButton('MuntjacTunes Store')
        muntjacTunesStore.setWidth('100%')
        purchased = NativeButton('Purchased')
        purchased.setWidth('100%')

        playlists = Label('Playlists')
        genius = NativeButton('Geniues')
        genius.setWidth('100%')
        recent = NativeButton('Recently Added')
        recent.setWidth('100%')

        # Lets add them to the 'selections' layout
        selections.addComponent(library)
        selections.addComponent(music)
        selections.addComponent(store)
        selections.addComponent(muntjacTunesStore)
        selections.addComponent(purchased)
        selections.addComponent(playlists)
        selections.addComponent(genius)
        selections.addComponent(recent)

        # Then add the selections to the sidebar, and set it expanding
        sidebar.addComponent(selections)
        sidebar.setExpandRatio(selections, 1.0)

        # Then comes the cover artwork (we'll add the actual image in the
        # themeing section)
        cover = Embedded('Currently Playing')
        sidebar.addComponent(cover)

        # And lastly, we need the track listing table It should fill the whole
        # left side of our bottom layout
        listing = Table()
        listing.setSizeFull()
        listing.setSelectable(True)
        bottom.setSecondComponent(listing)

        # Add the table headers
        listing.addContainerProperty('Name', str, '')
        listing.addContainerProperty('Time', str, '0:00')
        listing.addContainerProperty('Artist', str, '')
        listing.addContainerProperty('Album', str, '')
        listing.addContainerProperty('Genre', str, '')
        listing.addContainerProperty('Rating', NativeSelect, NativeSelect())

        # Lets populate the table with random data
        tracks = ['Red Flag', 'Millstone', 'Not The Sun', 'Breath',
                'Here We Are', 'Deep Heaven', 'Her Voice Resides',
                'Natural Tan', 'End It All', 'Kings', 'Daylight Slaving',
                'Mad Man', 'Resolve', 'Teargas', 'African Air', 'Passing Bird']
        times = ['4:12', '6:03', '5:43', '4:32', '3:42', '4:45', '2:56',
                '9:34', '2:10', '3:44', '5:49', '6:30', '5:18', '7:42',
                '3:13', '2:52']
        artists = ['Billy Talent', 'Brand New', 'Breaking Benjamin',
                'Becoming The Archetype', 'Bullet For My Valentine',
                'Chasing Victory', 'Chimaira', 'Danko Jones', 'Deadlock',
                'Deftones', 'From Autumn To Ashes', 'Haste The Day',
                'Four Year Strong', 'In Flames', 'Kemopetrol', 'John Legend']
        albums = ['Once Again', 'The Caitiff Choir', 'The Devil And God',
                'Light Grenades', 'Dicthonomy', 'Back In Black', 'Dreamer',
                'Come Clarity', 'Year Zero', 'Frames', 'Fortress', 'Phobia',
                'The Poison', 'Manifesto', 'White Pony', 'The Big Dirty']
        genres = ['Rock', 'Metal', 'Hardcore', 'Indie', 'Pop', 'Alternative',
                'Blues', 'Jazz', 'Hip Hop', 'Electronica', 'Punk', 'Hard Rock',
                'Dance', 'R\'n\'B', 'Gospel', 'Country']

        for i in range(100):
            s = NativeSelect()
            s.addItem('1 star')
            s.addItem('2 stars')
            s.addItem('3 stars')
            s.addItem('4 stars')
            s.addItem('5 stars')
            s.select('%d stars' % (i % 5))
            index = i % 16
            listing.addItem([tracks[index], times[index],
                    artists[index], albums[index], genres[index], s], i)

        # We'll align the track time column to right as well
        listing.setColumnAlignment('Time', Table.ALIGN_RIGHT)

        # TODO: the footer

        # Now what's left to do? Themeing of course.
        self.setTheme('vaadintunes')

        # Let's give a namespace to our application window. This way, if
        # someone uses the same theme for different applications, we don't
        # get unwanted style conflicts.
        root.setStyleName('tTunes')

        top.setStyleName('top')
        top.setHeight('75px')  # Same as the background image height

        playback.setStyleName('playback')
        playback.setMargin(False, True, False, False)  # Add right-side margin
        play.setStyleName('play')
        nextt.setStyleName('next')
        prev.setStyleName('prev')
        playback.setComponentAlignment(prev, Alignment.MIDDLE_LEFT)
        playback.setComponentAlignment(nextt, Alignment.MIDDLE_LEFT)

        volume.setStyleName('volume')
        mute.setStyleName('mute')
        maxx.setStyleName('max')
        vol.setWidth('78px')

        status.setStyleName('status')
        status.setMargin(True)
        status.setHeight('46px')  # Height of the background image

        toggleVisualization.setStyleName('toggle-vis')
        jumpToTrack.setStyleName('jump')

        viewAsTable.setStyleName('viewmode-table')
        viewAsGrid.setStyleName('viewmode-grid')
        coverflow.setStyleName('viewmode-coverflow')

        sidebar.setStyleName('sidebar')

        music.setStyleName('selected')

        cover.setSource(ThemeResource('images/album-cover.jpg'))
        # Because this is an image, it will retain it's aspect ratio
        cover.setWidth('100%')


if __name__ == '__main__':
    from muntjac.main import muntjac
    muntjac(MuntjacTunesLayout, nogui=True, forever=True, debug=True)
