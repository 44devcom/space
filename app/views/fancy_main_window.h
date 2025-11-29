#ifndef FANCY_MAIN_WINDOW_H
#define FANCY_MAIN_WINDOW_H

#include <QMainWindow>
#include "ui_fancy_main_window.h"
#include "background_3d_widget.h"
#include "loader_widget.h"

class FancyMainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit FancyMainWindow(QWidget *parent = nullptr);
    ~FancyMainWindow();

private slots:
    void on_action_exit_triggered();
    void on_action_settings_triggered();
    void on_action_about_triggered();

private:
    Ui::FancyMainWindow *ui;
    Background3DWidget *m_background_widget;
    LoaderWidget *m_loader_widget;
    void setup_ui();
    void setup_menu();
    void setup_animations();
};

#endif // FANCY_MAIN_WINDOW_H

