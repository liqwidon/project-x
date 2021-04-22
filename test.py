{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import sys\n",
    "\n",
    "from PyQt5 import uic\n",
    "from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout\n",
    "from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas\n",
    "\n",
    "import matplotlib.pyplot as plt\n",
    "import numpy as np"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "class Window(QMainWindow):\n",
    "    def __init__(self):\n",
    "        super(Window,self).__init__()\n",
    "        ui = uic.loadUi('form.ui', self)\n",
    "        self.click()\n",
    "        \n",
    "        self.figure = plt.Figure()\n",
    "        self.canvas = FigureCanvas(self.figure)\n",
    "        \n",
    "        layout = QVBoxLayout()\n",
    "        layout.addWidget(self.canvas)\n",
    "        self.w1.setLayout(layout)\n",
    "        #self.p()\n",
    "        \n",
    "    def click(self):\n",
    "        self.b1.clicked.connect(lambda: self.l1.setText(self.l1.text() + \" OMG\"))\n",
    "        self.b1.clicked.connect(self.p)\n",
    "        \n",
    "    def p(self):\n",
    "#         data = np.arange(-10,10)\n",
    "#         ax = self.figure.add_subplot(111)\n",
    "#         ax.clear()\n",
    "#         ax.plot(data, data)\n",
    "#         self.canvas.draw()\n",
    "        sizes = [17, 15, 11, 15, 14]\n",
    "        labels = []\n",
    "        explode = []\n",
    "        for i in range(len(sizes)):\n",
    "            string = 'Б03-91' + str(i+1)\n",
    "            labels.append(string)\n",
    "            explode.append(sizes[i] / 100)\n",
    "    \n",
    "#labels = ['Б03-911', 'Б03-912', 'Б03-913', 'Б03-914', 'Б03-915']\n",
    "#explode = (0.17, 0.15, 0.11, 0.15, 0.14)\n",
    "\n",
    "        ax1 = self.figure.add_subplot(1,1,1)\n",
    "        ax1.clear()\n",
    "        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',\n",
    "        shadow=True, startangle=20)\n",
    "        ax1.axis('equal')\n",
    "        ax1.legend(title = 'Номер группы')\n",
    "        self.canvas.draw()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "def main():\n",
    "    app = QApplication(sys.argv)\n",
    "    window = Window()\n",
    "    window.show()\n",
    "    sys.exit(app.exec_())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "<ipython-input-2-bf73da831bdc>:36: MatplotlibDeprecationWarning: Adding an axes using the same arguments as a previous axes currently reuses the earlier instance.  In a future version, a new instance will always be created and returned.  Meanwhile, this warning can be suppressed, and the future behavior ensured, by passing a unique label to each axes instance.\n",
      "  ax1 = self.figure.add_subplot(1,1,1)\n"
     ]
    },
    {
     "ename": "SystemExit",
     "evalue": "0",
     "output_type": "error",
     "traceback": [
      "An exception has occurred, use %tb to see the full traceback.\n",
      "\u001b[1;31mSystemExit\u001b[0m\u001b[1;31m:\u001b[0m 0\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\ProgramData\\Anaconda3\\lib\\site-packages\\IPython\\core\\interactiveshell.py:3351: UserWarning: To exit: use 'exit', 'quit', or Ctrl-D.\n",
      "  warn(\"To exit: use 'exit', 'quit', or Ctrl-D.\", stacklevel=1)\n"
     ]
    }
   ],
   "source": [
    "if __name__ == '__main__':\n",
    "     main()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
