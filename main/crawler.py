                try:
                    for root, dirs, files in os.walk('C:\\'):
                        if lookfor in files:
                            print ("found: %s" % join(root, lookfor))
                            tempPath = root
                            break
                    with open("mind.txt",'a') as w:
                        w.write(text+","+tempPath)
                except Exception:
                    for root, dirs, files in os.walk('Z:\\Programs'):
                        if lookfor in files:
                            print ("found: %s" % join(root, lookfor))
                            tempPath = root
                        break
                    with open("mind.txt",'a') as w:
                        w.write(text+","+tempPath)
                except Exception:
                    engine.say("Sorry, but I can't seem to find "+text+" Could you show me where it is?")
                    engine.runAndWait()
                    Tk().withdraw()
                    tempPath = askopenfilename()
                    with open("mind.txt",'a') as w:
                        w.write(text+","+tempPath)
                if tempPath != 'null':
                    os.system(x)
                throwaway = input("Press enter to resume...")
                loop = True
