import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';

import { AppLayout } from '../components/AppLayout';
import { FaqPage } from '../pages/FaqPage';
import { AffiliateDisclosurePage } from '../pages/AffiliateDisclosurePage';
import { DisclaimerPage } from '../pages/DisclaimerPage';
import { HomePage } from '../pages/HomePage';
import { IssueDetailPage } from '../pages/IssueDetailPage';
import { IssuesPage } from '../pages/IssuesPage';
import { NotFoundPage } from '../pages/NotFoundPage';
import { PatchDetailPage } from '../pages/PatchDetailPage';
import { PatchesPage } from '../pages/PatchesPage';
import { PrivacyPage } from '../pages/PrivacyPage';
import { SearchPage } from '../pages/SearchPage';
import { SettingsDoctorPage } from '../pages/SettingsDoctorPage';

export function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/ko" replace />} />
        <Route path="/ko" element={<AppLayout />}>
          <Route index element={<HomePage />} />
          <Route path="patches" element={<PatchesPage />} />
          <Route path="patches/:version" element={<PatchDetailPage />} />
          <Route path="issues" element={<IssuesPage />} />
          <Route path="issues/:slug" element={<IssueDetailPage />} />
          <Route path="faq" element={<FaqPage />} />
          <Route path="search" element={<SearchPage />} />
          <Route path="settings-doctor" element={<SettingsDoctorPage />} />
          <Route path="privacy" element={<PrivacyPage />} />
          <Route path="disclaimer" element={<DisclaimerPage />} />
          <Route path="affiliate-disclosure" element={<AffiliateDisclosurePage />} />
        </Route>
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </BrowserRouter>
  );
}
