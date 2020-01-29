const username = 'SVD_user_manage';
let dashboard, report, editor, visualDesigner;

module.exports = {

  'set a report to test SVD'(browser) {
    report = require(`../../testData/functionality/visualDesigner/basicReport/tenta69`);
    browser
      .setupReport(report)
      .createMockNormalUser(username)
      .assignFeatureToggleToUser(username, ['Reporting_StudioVisualDesigner'])
      .end(); // going to log in as newly created user
  },

  'login as new user and go to editor'(browser) {
    browser
      .grantAccessToReportById(browser.globals.testContext.reportId, 'Manage', username)
      .url(browser.globals.urls.r2)
      .loginToR2(username, browser.globals.users.mockUser.password)
      .goToReportEditor(browser.globals.testContext.reportId);
    editor = browser.page.EditorPage();
    dashboard = browser.page.DashboardPage();
    editor.verifyPage(false);
    visualDesigner = browser.page.VisualDesigner();
    visualDesigner.verifyDesigner();
  },

  'select a widget and open settings pane'() {
    visualDesigner.checkNumberOfWidgets(4);
    visualDesigner.editNthWidget(2);
  },

  'switching to preview should deselect a widget'() {
    visualDesigner.isWidgetSelected(2, true);
    editor.closePaneAndPreview();
    visualDesigner.isWidgetSelected(2, false);
  },
  'hover a widget and check menu buttons (goToCode, viewCDL, deleteWidget)'() {
    visualDesigner.verifyWidgetOverlayButtons(1);
    editor.activateEditMode();
    visualDesigner
      .verifyWidgetOverlayButtons(1, true)
      .goToCodeNthWidget(1)
      .closePanel()
      .editNthWidget(1)
      .closePanel()
      .deleteNthWidget(1);
  },
};
