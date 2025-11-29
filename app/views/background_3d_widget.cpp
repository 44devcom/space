#include "background_3d_widget.h"
#include <QOpenGLContext>
#include <cmath>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

Background3DWidget::Background3DWidget(QWidget *parent)
    : QOpenGLWidget(parent)
    , m_rotation_angle(0.0f)
{
    m_timer = new QTimer(this);
    connect(m_timer, &QTimer::timeout, this, [this]() {
        m_rotation_angle += 1.0f;
        if (m_rotation_angle >= 360.0f) {
            m_rotation_angle = 0.0f;
        }
        update();
    });
    m_timer->start(16); // ~60 FPS
}

Background3DWidget::~Background3DWidget()
{
    makeCurrent();
    doneCurrent();
}

void Background3DWidget::initializeGL()
{
    initializeOpenGLFunctions();
    
    glEnable(GL_DEPTH_TEST);
    glClearColor(0.1f, 0.1f, 0.15f, 1.0f);
}

void Background3DWidget::resizeGL(int w, int h)
{
    setup_projection(w, h);
}

void Background3DWidget::paintGL()
{
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    
    m_view.setToIdentity();
    m_view.translate(0.0f, 0.0f, -5.0f);
    m_view.rotate(m_rotation_angle, 0.0f, 1.0f, 0.0f);
    m_view.rotate(m_rotation_angle * 0.5f, 1.0f, 0.0f, 0.0f);
    
    m_model.setToIdentity();
    
    draw_cube();
}

void Background3DWidget::setup_projection(int width, int height)
{
    glViewport(0, 0, width, height);
    
    m_projection.setToIdentity();
    float aspect = static_cast<float>(width) / static_cast<float>(height);
    m_projection.perspective(45.0f, aspect, 0.1f, 100.0f);
}

void Background3DWidget::draw_cube()
{
    // Use modern OpenGL approach with shaders or fallback to immediate mode
    // For compatibility, using immediate mode (deprecated but works on most systems)
    
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    float aspect = static_cast<float>(width()) / static_cast<float>(height());
    glFrustum(-aspect * 0.5f, aspect * 0.5f, -0.5f, 0.5f, 0.1f, 100.0f);
    
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    glTranslatef(0.0f, 0.0f, -5.0f);
    glRotatef(m_rotation_angle, 0.0f, 1.0f, 0.0f);
    glRotatef(m_rotation_angle * 0.5f, 1.0f, 0.0f, 0.0f);
    
    // Draw wireframe cube
    glColor3f(0.3f, 0.6f, 1.0f);
    glLineWidth(2.0f);
    
    glBegin(GL_LINES);
    
    // Front face
    glVertex3f(-1.0f, -1.0f,  1.0f);
    glVertex3f( 1.0f, -1.0f,  1.0f);
    glVertex3f( 1.0f, -1.0f,  1.0f);
    glVertex3f( 1.0f,  1.0f,  1.0f);
    glVertex3f( 1.0f,  1.0f,  1.0f);
    glVertex3f(-1.0f,  1.0f,  1.0f);
    glVertex3f(-1.0f,  1.0f,  1.0f);
    glVertex3f(-1.0f, -1.0f,  1.0f);
    
    // Back face
    glVertex3f(-1.0f, -1.0f, -1.0f);
    glVertex3f( 1.0f, -1.0f, -1.0f);
    glVertex3f( 1.0f, -1.0f, -1.0f);
    glVertex3f( 1.0f,  1.0f, -1.0f);
    glVertex3f( 1.0f,  1.0f, -1.0f);
    glVertex3f(-1.0f,  1.0f, -1.0f);
    glVertex3f(-1.0f,  1.0f, -1.0f);
    glVertex3f(-1.0f, -1.0f, -1.0f);
    
    // Connecting edges
    glVertex3f(-1.0f, -1.0f,  1.0f);
    glVertex3f(-1.0f, -1.0f, -1.0f);
    glVertex3f( 1.0f, -1.0f,  1.0f);
    glVertex3f( 1.0f, -1.0f, -1.0f);
    glVertex3f( 1.0f,  1.0f,  1.0f);
    glVertex3f( 1.0f,  1.0f, -1.0f);
    glVertex3f(-1.0f,  1.0f,  1.0f);
    glVertex3f(-1.0f,  1.0f, -1.0f);
    
    glEnd();
}

