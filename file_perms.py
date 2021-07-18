import win32security
import win32file
import os


class file_perms:

    def getFileACL(self, fileName):
        myPath = fileName
        """
        Get Access Control List of a file/directory
        @return: PyACL object
        """
        info = win32security.DACL_SECURITY_INFORMATION
        sd = win32security.GetFileSecurity(myPath, info)
        acl = sd.GetSecurityDescriptorDacl()
        return acl

    def grantAccessToFile(self, filePath, userName='everyone'):
        """
        Allow Permission to userName on a file/directory
        @param file: path of the file/dir
        @param userName: name of the user to add to the acl of the file/dir
        """
        #self.logger.info('Granting access to file %s' % filePath)
        import ntsecuritycon as con
        if os.path.isfile(filePath) or os.path.isdir(filePath):

            info = win32security.DACL_SECURITY_INFORMATION
            sd = win32security.GetFileSecurity(filePath, info)
            acl = self.getFileACL(filePath)
            user, domain, acType = win32security.LookupAccountName("", userName)

            acl.AddAccessAllowedAce(win32security.ACL_REVISION, con.FILE_GENERIC_READ | con.DELETE, user)
            sd.SetSecurityDescriptorDacl(1, acl, 0)
            win32security.SetFileSecurity(filePath, win32security.DACL_SECURITY_INFORMATION, sd)

        else:
            #self.logger.info('File/Directory %s is not valid' % filePath)

            raise IOError('FilePath %s does not exist' % filePath)