#include <QApplication>
#include "views/fancy_main_window.h"

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    
    FancyMainWindow window;
    window.show();
    
    return app.exec();
}

