from pynput.mouse import Button, Controller
mouse = Controller()
mouse.position = (300, 300)
mouse.click(Button.left)