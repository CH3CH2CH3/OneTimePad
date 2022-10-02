import PySimpleGUI as sg

n = 0
n1 = 0

sg.theme('Dark Grey 13')

tab1_layout = [[sg.Text("Choose files:")],
               [sg.Text('Plain Text', size=(15, 1)), sg.Input(key='-PLATXT-', size=(35), do_not_clear=False),
                sg.FileBrowse(file_types=(("Text Files", "*.txt"),))],
               [sg.Text('Key', size=(15, 1)), sg.Input(key='-KEY1-', size=(35), do_not_clear=False),
                sg.FileBrowse(file_types=(("Text Files", "*.txt"),))],
               [sg.Submit(key='-SUB1-')]]

tab2_layout = [[sg.Text("Choose files:")],
               [sg.Text('Cipher Text', size=(15, 1)), sg.Input(key='-CIPTXT-', size=(35), do_not_clear=False),
                sg.FileBrowse(file_types=(("Text Files", "*.txt"),))],
               [sg.Text('Key', size=(15, 1)), sg.Input(key='-KEY2-', size=(35), do_not_clear=False),
                sg.FileBrowse(file_types=(("Text Files", "*.txt"),))],
               [sg.Submit(key='-SUB2-')]]

tab3_layout = [[sg.Text('The Key and Plaintext must both be in the .txt format')],
               [sg.Text('The Key may consist only of lowercase Latin characters')],
               [sg.Text('The Plaintext may only consist of lowercase Latin characters and spaces.')],
               [sg.Text('This means no punctuation allowed.')],
               [sg.Text('Punctuation can be replaced with the word. i.e. "." to "fullstop"')]]

layout = [[sg.TabGroup([[sg.Tab('Encryption', tab1_layout), sg.Tab('Decryption', tab2_layout),
           sg.Tab('?', tab3_layout)]])],
          [sg.Button('Exit')]]

window = sg.Window('One Time Pad', layout, default_element_size=(12, 1), size=(500, 210),
                   icon="greencircle.ico")

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == '-SUB1-':
        plaintxt_path, keytxt_path = values['-PLATXT-'], values['-KEY1-']
        with(
            open(plaintxt_path) as ptxt,
            open(keytxt_path) as ktxt,
            open(f"CiphertextOut{n}.txt", "a") as ctxt
        ):
            while True:
                cin = ptxt.read()
                ckey = ktxt.read()
                if len(cin) <= len(ckey):
                    for x, y in zip(cin, ckey):
                        ncin = ord(x)
                        if ncin == 32:
                            ncin = 0
                        else:
                            ncin -= 96
                        nckey = ord(y)-96
                        nout = ncin + nckey
                        mnout = nout%27
                        out = chr(mnout+96)
                        ctxt.write(out)
                    else:
                        sg.popup('Ciphertext creation was successful.', title='Success')
                        n += 1
                        break
                elif len(cin) > len(ckey):
                    sg.popup('Key length is not greater or equal to length of Plaintext.', title='Error')
                    break
                else:
                    sg.popup('Unknown Error', title='Error')
                    break
            continue
    if event == '-SUB2-':
        ciphertxt_path, keytxt_path = values['-CIPTXT-'], values['-KEY2-']
        with(
            open(ciphertxt_path) as ctxt,
            open(keytxt_path) as ktxt,
            open(f"PlaintextOut{n1}.txt", "a") as ptxt
        ):
            while True:
                cin = ctxt.read()
                ckey = ktxt.read()
                for x, y in zip(cin, ckey):
                    ncin = ord(x)-96
                    nckey = ord(y)-96
                    nout = ncin - nckey
                    if nout == 0:
                        out = chr(32)
                    else:
                        mout = nout%27
                        out = chr((mout+96))
                    ptxt.write(out)
                else:
                    sg.popup('Plaintext creation was successful.', title='Success')
                    n1 += 1
                    break
            continue

window.close()
