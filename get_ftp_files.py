#!/usr/bin/env python
# The naming convention for individual documents is: <bill chamber><bill type><bill suffix><bill version>
# # File Name   Description
# # <bill chamber>  H=House, S=Senate
# # <bill type> B=Bill, J=Joint Resolution, R=Resolution, C=Concurrent Resolution
# # <bill suffix>   5-digit number
# # <bill version>  I=Introduced, S=Senate Committee Report, H=House Committee Report, E=Engrossed, F=Enrolled
#
ftp = FTP('ftp.legis.state.tx.us')
ftp.login()

#Directory structure: /bills/<legislative session>/<document type>/<text format>/<bill type>/<grouping of 100 bills>
ftp.cwd('/bills/851/billtext/html/house_bills/HB00001_HB00099')
files = ftp.nlst()

local_dir = '~/remote/bills/tx/data/html'

for file in files:
    try:
        local_filename = os.path.join(local_dir, file)
        print "Getting filename " + file
        ftp.retrbinary('RETR %s' % file, open(local_filename, 'wb').write)
        print "Saving at %s" % local_filename
    except Exception, err:
        print err
#         if (is_empty(local_filename)):
#             os.remove(local_filename)
        continue
