'''
Created on May 29, 2016

@author: davidlepage
'''
import sys, traceback
from parser import CLIParser, ArgumentParserError
from options import all_arg_names
import smc.actions.create

class SMCBroker(object):
    def __init__(self, document):
        self.document = document #str from cli       
        mangle_args = all_arg_names()
        self.document = ['--'+cmd if cmd in mangle_args else cmd for cmd in self.document]

    def validate(self):
        """ wrapper around argparse so it doesn't kill the shell """
        if self.document:           
            try:
                parser = CLIParser(self.document)
                self.document = parser.document
                action = self.document.get('action') and self.document.pop('action', None) #remove not needed attrs
                target = self.document.get('target') and self.document.pop('target', None)
                try:
                    if action == 'create':
                        getattr(smc.actions.create, target)(**self.document) #dispatch
                    elif action == 'remove':
                        getattr(smc.actions.remove, target)(**self.document) #dispatch
                except Exception, e:
                    traceback.print_exc(file=sys.stdout)
                                
            except ArgumentParserError, e: #missing arguments
                return "Incorrect syntax, %s" % e
            except AttributeError, e: #incorrect argument given
                return "Invalid command"
            except SystemExit: #argparse does a sys.exit after running -h
                print "Stopping exit"
                pass
        

if __name__ == "__main__":
    try:
        executor = SMCBroker(['remove', 'element', '--name', 'efwe'])
        
        executor.validate()
    except Exception, e:
        print "Exception: %s" % e 
        