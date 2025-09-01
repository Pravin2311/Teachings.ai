// pages/api/send-notification.js
import { WebPush } from 'web-push';

// Set VAPID keys from Vercel environment variables
if (!WebPush.vapidDetails) {
  WebPush.setVapidDetails(
    'mailto:admin@teachings.ai',
    process.env.NEXT_PUBLIC_VAPID_PUBLIC_KEY,
    process.env.VAPID_PRIVATE_KEY
  );
}

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { subscription, title, body, url } = req.body;

  if (!subscription || !title || !body) {
    return res.status(400).json({ error: 'Missing required fields' });
  }

  const payload = JSON.stringify({
    title,
    body,
    url: url || '/'
  });

  try {
    await WebPush.sendNotification(subscription, payload);
    return res.status(200).json({ success: true });
  } catch (error) {
    console.error('Push error:', error);
    return res.status(500).json({ error: 'Failed to send notification' });
  }
}