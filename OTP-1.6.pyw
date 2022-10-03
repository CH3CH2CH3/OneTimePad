import PySimpleGUI as sg

n = 0
n1 = 0

sg.theme('Dark Grey 13')

tab1_layout = [[sg.T("Choose files:")],
               [sg.T('Plain Text', size=(15, 1)), sg.I(key='-PLATXT-', size=(35), do_not_clear=False),
                sg.FileBrowse(file_types=(("Text Files", "*.txt"),))],
               [sg.T('Key', size=(15, 1)), sg.I(key='-KEY1-', size=(35), do_not_clear=False),
                sg.FileBrowse(file_types=(("Text Files", "*.txt"),))],
               [sg.Submit(key='-SUB1-')]]

tab2_layout = [[sg.T("Choose files:")],
               [sg.T('Cipher Text', size=(15, 1)), sg.I(key='-CIPTXT-', size=(35), do_not_clear=False),
                sg.FileBrowse(file_types=(("Text Files", "*.txt"),))],
               [sg.T('Key', size=(15, 1)), sg.I(key='-KEY2-', size=(35), do_not_clear=False),
                sg.FileBrowse(file_types=(("Text Files", "*.txt"),))],
               [sg.Submit(key='-SUB2-')]]

tab3_layout = [[sg.T('The Key and Plaintext must both be in the .txt format')],
               [sg.T('The Key and Plaintext may consist only of ASCII characters')],
               [sg.T('The Key must be at least as long as the Plaintext')]]

layout = [[sg.TabGroup([[sg.Tab('Encryption', tab1_layout), sg.Tab('Decryption', tab2_layout),
                         sg.Tab('?', tab3_layout)]])],
          [sg.Button('Exit')]]

window = sg.Window('One Time Pad', layout, default_element_size=(12, 1), size=(500, 200),
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
                        out = chr((((ord(x) - 32) + (ord(y) - 32)) % 95) + 32)
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
                    out = chr((((ord(x) - 32) - (ord(y) - 32)) % 95) + 32)
                    ptxt.write(out)
                else:
                    sg.popup('Plaintext creation was successful.', title='Success')
                    n1 += 1
                    break
            continue

window.close()
