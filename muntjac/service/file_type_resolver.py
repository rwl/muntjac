# Copyright (C) 2012 Vaadin Ltd. 
# Copyright (C) 2012 Richard Lincoln
# 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
# 
#     http://www.apache.org/licenses/LICENSE-2.0 
# 
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License.

"""Defines a class that can figure out mime-types and icons related to
files."""

from os.path import isdir

from muntjac.terminal.theme_resource import ThemeResource


class FileTypeResolver(object):
    """Utility class that can figure out mime-types and icons related to files.

    Note : The icons are associated purely to mime-types, so a file may not
    have a custom icon accessible with this class.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    #: Default icon given if no icon is specified for a mime-type.
    DEFAULT_ICON = ThemeResource('../runo/icons/16/document.png')

    #: Default mime-type.
    DEFAULT_MIME_TYPE = 'application/octet-stream'

    #: Initial file extension to mime-type mapping.
    _initialExtToMIMEMap = \
            ('application/cu-seeme                            csm cu,'
             'application/dsptype                             tsp,'
             'application/futuresplash                        spl,'
             'application/mac-binhex40                        hqx,'
             'application/msaccess                            mdb,'
             'application/msword                              doc dot,'
             'application/octet-stream                        bin,'
             'application/oda                                 oda,'
             'application/pdf                                 pdf,'
             'application/pgp-signature                       pgp,'
             'application/postscript                          ps ai eps,'
             'application/rtf                                 rtf,'
             'application/vnd.ms-excel                        xls xlb,'
             'application/vnd.ms-powerpoint                   ppt pps pot,'
             'application/vnd.wap.wmlc                        wmlc,'
             'application/vnd.wap.wmlscriptc                  wmlsc,'
             'application/wordperfect5.1                      wp5,'
             'application/zip                                 zip,'
             'application/x-123                               wk,'
             'application/x-bcpio                             bcpio,'
             'application/x-chess-pgn                         pgn,'
             'application/x-cpio                              cpio,'
             'application/x-debian-package                    deb,'
             'application/x-director                          dcr dir dxr,'
             'application/x-dms                               dms,'
             'application/x-dvi                               dvi,'
             'application/x-xfig                              fig,'
             'application/x-font                              pfa pfb gsf pcf pcf.Z,'
             'application/x-gnumeric                          gnumeric,'
             'application/x-gtar                              gtar tgz taz,'
             'application/x-hdf                               hdf,'
             'application/x-httpd-php                         phtml pht php,'
             'application/x-httpd-php3                        php3,'
             'application/x-httpd-php3-source                 phps,'
             'application/x-httpd-php3-preprocessed           php3p,'
             'application/x-httpd-php4                        php4,'
             'application/x-ica                               ica,'
             'application/x-java-archive                      jar,'
             'application/x-java-serialized-object            ser,'
             'application/x-java-vm                           class,'
             'application/x-javascript                        js,'
             'application/x-kchart                            chrt,'
             'application/x-killustrator                      kil,'
             'application/x-kpresenter                        kpr kpt,'
             'application/x-kspread                           ksp,'
             'application/x-kword                             kwd kwt,'
             'application/x-latex                             latex,'
             'application/x-lha                               lha,'
             'application/x-lzh                               lzh,'
             'application/x-lzx                               lzx,'
             'application/x-maker                             frm maker frame fm fb book fbdoc,'
             'application/x-mif                               mif,'
             'application/x-msdos-program                     com exe bat dll,'
             'application/x-msi                               msi,'
             'application/x-netcdf                            nc cdf,'
             'application/x-ns-proxy-autoconfig               pac,'
             'application/x-object                            o,'
             'application/x-ogg                               ogg,'
             'application/x-oz-application                    oza,'
             'application/x-perl                              pl pm,'
             'application/x-pkcs7-crl                         crl,'
             'application/x-redhat-package-manager            rpm,'
             'application/x-shar                              shar,'
             'application/x-shockwave-flash                   swf swfl,'
             'application/x-star-office                       sdd sda,'
             'application/x-stuffit                           sit,'
             'application/x-sv4cpio                           sv4cpio,'
             'application/x-sv4crc                            sv4crc,'
             'application/x-tar                               tar,'
             'application/x-tex-gf                            gf,'
             'application/x-tex-pk                            pk PK,'
             'application/x-texinfo                           texinfo texi,'
             'application/x-trash                             ~ % bak old sik,'
             'application/x-troff                             t tr roff,'
             'application/x-troff-man                         man,'
             'application/x-troff-me                          me,'
             'application/x-troff-ms                          ms,'
             'application/x-ustar                             ustar,'
             'application/x-wais-source                       src,'
             'application/x-wingz                             wz,'
             'application/x-x509-ca-cert                      crt,'
             'audio/basic                                     au snd,'
             'audio/midi                                      mid midi,'
             'audio/mpeg                                      mpga mpega mp2 mp3,'
             'audio/mpegurl                                   m3u,'
             'audio/prs.sid                                   sid,'
             'audio/x-aiff                                    aif aiff aifc,'
             'audio/x-gsm                                     gsm,'
             'audio/x-pn-realaudio                            ra rm ram,'
             'audio/x-scpls                                   pls,'
             'audio/x-wav                                     wav,'
             'audio/ogg                                       ogg,'
             'audio/mp4                                       m4a,'
             'audio/x-aac                                     aac,'
             'image/bitmap                                    bmp,'
             'image/gif                                       gif,'
             'image/ief                                       ief,'
             'image/jpeg                                      jpeg jpg jpe,'
             'image/pcx                                       pcx,'
             'image/png                                       png,'
             'image/svg+xml                                   svg svgz,'
             'image/tiff                                      tiff tif,'
             'image/vnd.wap.wbmp                              wbmp,'
             'image/x-cmu-raster                              ras,'
             'image/x-coreldraw                               cdr,'
             'image/x-coreldrawpattern                        pat,'
             'image/x-coreldrawtemplate                       cdt,'
             'image/x-corelphotopaint                         cpt,'
             'image/x-jng                                     jng,'
             'image/x-portable-anymap                         pnm,'
             'image/x-portable-bitmap                         pbm,'
             'image/x-portable-graymap                        pgm,'
             'image/x-portable-pixmap                         ppm,'
             'image/x-rgb                                     rgb,'
             'image/x-xbitmap                                 xbm,'
             'image/x-xpixmap                                 xpm,'
             'image/x-xwindowdump                             xwd,'
             'text/comma-separated-values                     csv,'
             'text/css                                        css,'
             'text/html                                       htm html xhtml,'
             'text/mathml                                     mml,'
             'text/plain                                      txt text diff,'
             'text/richtext                                   rtx,'
             'text/tab-separated-values                       tsv,'
             'text/vnd.wap.wml                                wml,'
             'text/vnd.wap.wmlscript                          wmls,'
             'text/xml                                        xml,'
             'text/x-c++hdr                                   h++ hpp hxx hh,'
             'text/x-c++src                                   c++ cpp cxx cc,'
             'text/x-chdr                                     h,'
             'text/x-csh                                      csh,'
             'text/x-csrc                                     c,'
             'text/x-java                                     java,'
             'text/x-moc                                      moc,'
             'text/x-pascal                                   p pas,'
             'text/x-setext                                   etx,'
             'text/x-sh                                       sh,'
             'text/x-tcl                                      tcl tk,'
             'text/x-tex                                      tex ltx sty cls,'
             'text/x-vcalendar                                vcs,'
             'text/x-vcard                                    vcf,'
             'video/dl                                        dl,'
             'video/fli                                       fli,'
             'video/gl                                        gl,'
             'video/mpeg                                      mpeg mpg mpe,'
             'video/quicktime                                 qt mov,'
             'video/x-mng                                     mng,'
             'video/x-ms-asf                                  asf asx,'
             'video/x-msvideo                                 avi,'
             'video/x-sgi-movie                               movie,'
             'video/ogg                                       ogv,'
             'video/mp4                                       mp4,'
             'x-world/x-vrml                                  vrm vrml wrl')


    #: File extension to MIME type mapping. All extensions are in lower case.
    _extToMIMEMap = dict()

    #: MIME type to Icon mapping.
    _MIMEToIconMap = dict()


    @classmethod
    def getMIMEType(cls, file_or_filename):
        """Gets the mime-type of a file. Currently the mime-type is resolved
        based only on the file name extension.

        @param file_or_filename:
                   the file or name of the file whose mime-type is requested.
        @return: mime-type string
        """
        # Checks for nulls
        if isinstance(file_or_filename, basestring):
            fileName = file_or_filename
            # Calculates the extension of the file
            dotIndex = fileName.find('.')
            while dotIndex >= 0 and fileName.find('.', dotIndex + 1) >= 0:
                dotIndex = fileName.find('.', dotIndex + 1)
            dotIndex += 1
            if len(fileName) > dotIndex:
                ext = fileName[dotIndex:]
                # Ignore any query parameters
                queryStringStart = ext.find('?')
                if queryStringStart > 0:
                    ext = ext[:queryStringStart]
                # Return type from extension map, if found
                typ = cls._extToMIMEMap.get(ext.lower())
                if typ is not None:
                    return typ
            return cls.DEFAULT_MIME_TYPE
        else:
            raise NotImplementedError

            fd = file_or_filename
            if fd is None:
                raise ValueError, 'File can not be null'
            # Directories
            if isdir(fd):
                # Drives
                if fd.getParentFile() is None:
                    return 'inode/drive'
                else:
                    return 'inode/directory'
            # Return type from extension
            return cls.getMIMEType(fd.getName())


    @classmethod
    def getIcon(cls, file_or_filename):
        """Gets the descriptive icon representing file, based on the filename.
        First the mime-type for the given filename is resolved, and then the
        corresponding icon is fetched from the internal icon storage. If it is
        not found the default icon is returned.

        @param file_or_filename:
                   the file or name of the file whose icon is requested.
        @return: the icon corresponding to the given file
        """
        return cls.getIconByMimeType(cls.getMIMEType(file_or_filename))


    @classmethod
    def getIconByMimeType(cls, mimeType):
        icon = cls._MIMEToIconMap.get(mimeType)
        if icon is not None:
            return icon

        # If nothing is known about the file-type, general file
        # icon is used
        return cls.DEFAULT_ICON


    @classmethod
    def addExtension(cls, extension, MIMEType):
        """Adds a mime-type mapping for the given filename extension. If the
        extension is already in the internal mapping it is overwritten.

        @param extension:
                   the filename extension to be associated with
                   C{MIMEType}.
        @param MIMEType:
                   the new mime-type for C{extension}.
        """
        cls._extToMIMEMap[extension.lower()] = MIMEType


    @classmethod
    def addIcon(cls, MIMEType, icon):
        """Adds a icon for the given mime-type. If the mime-type also has a
        corresponding icon, it is replaced with the new icon.

        @param MIMEType:
                   the mime-type whose icon is to be changed.
        @param icon:
                   the new icon to be associated with C{MIMEType}.
        """
        cls._MIMEToIconMap[MIMEType] = icon


    @classmethod
    def getExtensionToMIMETypeMapping(cls):
        """Gets the internal file extension to mime-type mapping.

        @return: unmodifiable map containing the current file extension to
                mime-type mapping
        """
        return dict(cls._extToMIMEMap)


    @classmethod
    def getMIMETypeToIconMapping(cls):
        """Gets the internal mime-type to icon mapping.

        @return: map containing the current mime-type to icon mapping
        """
        return dict(cls._MIMEToIconMap)


# Initialize extension to MIME map
lines = FileTypeResolver._initialExtToMIMEMap.split(',')
for line in lines:
    exts = line.split()
    typ = exts[0]
    for ext in exts[1:]:
        FileTypeResolver.addExtension(ext, typ)

# Initialize Icons
folder = ThemeResource('../runo/icons/16/folder.png')
FileTypeResolver.addIcon('inode/drive', folder)
FileTypeResolver.addIcon('inode/directory', folder)
