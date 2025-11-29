#include "fancy_main_window.h"
#include <QMessageBox>
#include <QPropertyAnimation>
#include <QEasingCurve>
#include <QVBoxLayout>

FancyMainWindow::FancyMainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::FancyMainWindow)
    , m_background_widget(nullptr)
    , m_loader_widget(nullptr)
{
    ui->setupUi(this);
    setup_ui();
    setup_menu();
    setup_animations();
}

FancyMainWindow::~FancyMainWindow()
{
    delete ui;
}

void FancyMainWindow::setup_ui()
{
    // Set fixed size to 1080x480
    setFixedSize(1080, 480);
    
    // Create 3D background widget
    m_background_widget = new Background3DWidget(ui->central_widget);
    m_background_widget->setGeometry(0, 0, 1080, 480);
    m_background_widget->lower(); // Put it behind other widgets
    
    // Create loader widget
    m_loader_widget = new LoaderWidget(ui->central_widget);
    m_loader_widget->move(510, 210); // Center position (1080/2 - 30, 480/2 - 30)
    m_loader_widget->raise(); // Put it on top
    m_loader_widget->start_animation();
    
    // Set window properties
    setWindowTitle(tr("Fancy Main Window"));
}

void FancyMainWindow::setup_menu()
{
    // Menu is already set up in UI file
    // Connect actions if needed
}

void FancyMainWindow::setup_animations()
{
    // Fade-in animation for loader
    QPropertyAnimation *fade_animation = new QPropertyAnimation(m_loader_widget, "windowOpacity", this);
    fade_animation->setDuration(1000);
    fade_animation->setStartValue(0.0);
    fade_animation->setEndValue(1.0);
    fade_animation->setEasingCurve(QEasingCurve::InOutQuad);
    fade_animation->start();
}

void FancyMainWindow::on_action_exit_triggered()
{
    close();
}

void FancyMainWindow::on_action_settings_triggered()
{
    QMessageBox::information(this, tr("Settings"), tr("Settings dialog will be implemented here."));
}

void FancyMainWindow::on_action_about_triggered()
{
    QMessageBox::about(this, tr("About"), 
        tr("Fancy Main Window\n\n"
           "A Qt C++ application with 3D animated background and loader."));
}

