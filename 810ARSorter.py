print('Running...')
from glob import glob
from time import sleep
from datetime import datetime
from itertools import cycle
import pyautogui
from pyscreeze import ImageNotFoundException

#pyinstaller -F 810ARSorter.py

## this code will need compiled once for each user
## dont forget about the windows dependant operating system stuff below


# ################################# #
# This is where you'll specify user #
# for the Reports folder path       #
# ################################# #
#user='ZVANMETER'
user='LORI'
#user='SGRADY'


# ################################# #
# This is where you'll specify temp #
# output folder for your .txt files #
# as well as your reports path      #
# ################################# #
txtpath='\\\\TMFSVR9\\EpicorData\\EDIData\\Live\\Out\\810Process\\'
xmlpath='\\\\TMFSVR9\\EpicorData\\Reports\\%s\\'%(user)


# ################################# #
# This is where you'll specify your #
# screenshot folder. You may need   #
# to produce these yourself         #
# ################################# #
path = 'Resources - 810ARSorter\\'		# For Win 7
#path = 'Resources - 810ARSorter - Win 10\\'	# For Win 10



# ###################################
#####################################
# ###################################
#####################################


def GenTxtInvoiceNum(lines):	#invoiceNum = GenTxtInvoiceNum(lines)
		#Parse Successful .txt files in temp output folder
	invoiceNum = ''
	for line in lines:
		if '~SHP~~' in line:
			head, sep, tail = line.partition('~SHP~~')
			invoiceNum, sep, tail = tail.partition('~')
			break
	return invoiceNum
	
def GenInvoiceNum(lines):		#invoiceNum, invoiceDate = GenInvoiceNum(lines)
		#Parse all lines within the given .xml file
	invoiceDate = ''
	for line in lines:
		if '<InvoiceNum>' in line:
			invoiceNum = line.strip().replace('<InvoiceNum>','').replace('</InvoiceNum>','')
			break
	for line in lines:
		if '<InvoiceDate>' in line:
			invoiceDate = line.strip().replace('<InvoiceDate>','').replace('</InvoiceDate>','')
			break
	return invoiceNum, invoiceDate

def GenProblems():
		# Discovers discrepencies between produced 
		# .txt files and .xml files
		
		# Check .txt
	txtlist = glob(txtpath+'*.txt')
	alltxtlist = {}
	for item in txtlist:
		with open(item, 'r') as f:
			lines=f.readlines()
		head, sep, file = item.replace('.txt','').partition('AR Invoice Form')
		invoiceNum = GenTxtInvoiceNum(lines)
		alltxtlist[invoiceNum] = file
	
		# Check .xml
	xmllist = glob(xmlpath+'AR Invoice Form*.xml')	
	allxmllist = {}
	for item in xmllist:
		with open(item, 'r') as f:
			lines=f.readlines()
		head, sep, file = item.replace('.XML','').partition('AR Invoice Form')
		invoiceNum, invoiceDate = GenInvoiceNum(lines)
		allxmllist[invoiceNum] = file
		
		# Compare
	problemlist = {}
	for xmlinvoiceNum, xmlvalue in allxmllist.items():
		found = False
		for txtinvoiceNum, txtvalue in alltxtlist.items():
			if txtinvoiceNum == xmlinvoiceNum:
				found = True
		if found == False:
			problemlist[xmlinvoiceNum] = xmlvalue
	return problemlist, allxmllist, alltxtlist
	
def DoOutput(problemlist, allxmllist, alltxtlist):	
	with open('Output.txt', 'w') as f:
	
			# Build messages
		today = datetime.now().strftime('%Y-%m-%d')
		xmlCount = str(len(allxmllist))
		txtCount = str(len(alltxtlist))
		problemCount = str(len(problemlist))
		txtTotal = str(len(problemlist)+len(alltxtlist))
		line1='Today\'s Date: '+today
		line2='Total Invoice XML Files: %s'%(xmlCount)
		line3='Total Invoice TXT Files: %s, Found TXT Files %s, Missing TXT Files %s'%(txtTotal,txtCount,problemCount)
		line4='Invoice Number : Invoice Date'
		
			# Display messages
		print(line1)
		print(line2)
		print(line3)
		print()
		print(line4)
			
			# Record messages
		f.write(line1+'\n')
		f.write(line2+'\n')
		f.write(line3+'\n'+'\n')
		f.write(line4+'\n')
	
		# Tells you how many iterations of macro it will preform
	print(len(problemlist), 'records missing')
	
		
	macrolist = []	
	
		# Build Generate Invoice Numbers
	for problem, file in problemlist.items():
		with open(xmlpath+'AR Invoice Form'+file+'.xml', 'r') as f:
			lines=f.readlines()
		invoiceNum, invoiceDate = GenInvoiceNum(lines)
		
			# Add Invoice Number to Macro Iterator
		macrolist.append(invoiceNum)
		
			# Display and Record 
		print(invoiceNum+' : '+invoiceDate)
		with open('Output.txt', 'a') as f:
			f.write(invoiceNum+' : '+invoiceDate+'\n')
	macrolist = list(set(macrolist))	
	return macrolist

def MacroSeq(item):
	print('\n',item)
		# Collect and format Images for macro operation
	imagelist = glob('%s*.png'%(path))
	imagecycle = cycle(imagelist)
	
	CycleImages(imagecycle,item)
	
def FindImage(filename):
	while True:
		try:
			x, y = pyautogui.locateCenterOnScreen(filename)
			return x, y
		except ImageNotFoundException as e:
			pass
			
def CycleImages(imagecycle,item):
	while True:
		filename = next(imagecycle)
		print(filename.replace(path,''))
		buttonx, buttony = FindImage(filename)
		if filename.replace(path,'')[0:1] == 'A':
			if filename.replace(path,'')[0:3] == 'AAA':
					# double click entry box, delete contents
				pyautogui.click(buttonx, buttony+35)
				pyautogui.click(buttonx, buttony+35)
				pyautogui.press('backspace')
				
					# Type InvoiceNum
				pyautogui.typewrite(item, interval=0.25)
				
					# Load Invoice
				pyautogui.press('tab')
			elif filename.replace(path,'')[0:3] == 'AAB':	
					# Open Print Menu
				pyautogui.click(buttonx, buttony)
			
			elif filename.replace(path,'')[0:3] == 'AAC':	
					# Open Dropdown Tab, and select report type
				pyautogui.click(buttonx+100, buttony)
				pyautogui.press('s')
				
			elif filename.replace(path,'')[0:3] == 'AAD':	
					# Select EPI810
				pyautogui.click(buttonx, buttony)
			elif filename.replace(path,'')[0:3] == 'AAE':	
					# Print preview
				pyautogui.click(buttonx+25, buttony)
			elif filename.replace(path,'')[0:3] == 'AAF':	
					# Exit Print Menu
				pyautogui.click(buttonx+80, buttony-95)
				
				print('Loop Finished, Breaking')
				break
	
def main():
		# Generate Workload
	problemlist, allxmllist, alltxtlist = GenProblems()
	print('found %s/%s files'%(len(allxmllist),len(alltxtlist)))
	
		# Terminate if all prints are successful
	if len(problemlist) == 0:
		return False
	
		# figure out which invoices numbers need resubmitted
	macrolist = DoOutput(problemlist, allxmllist, alltxtlist)
	
	for item in macrolist:
			# Manually enter the numbers, click all of the buttons
		MacroSeq(item)
		
		# Let the PrepLoop know to double check
	return True

def PrepLoop():
	try:
		FoundResults = main()
		if FoundResults == True:
			print('Double checking our files after this countdown.')
			for x in range(60):
				sleep(1)
				print(str(60-x)+'...', end="\r")
		FoundResults = main()
		if FoundResults == True:
			FoundResults = PrepLoop()
		else:
			print('No more results! Goodbye.')
	except Exception as e:
		print(e, 'All Function Ended')
		print('Did you forget to put the image folder in with this file?')
		
if __name__ == '__main__':
	try:
		print('This program will take control of your mouse and keyboard. If you need to regain control, rapidly drag your mouse pointer to the upper left corner of your screen')
		print('If your name is not listed on this program\'s name, it will not function for you.')
		PrepLoop()
	except Exception as e:
		print('An error has occured:', e)
	
	# This loop will keep the Console window open in compiled versions
	# so that you can read errors and such
while True:
	sleep(1)

